# DVC training job. This is a batch/one-off task, not a long-running service:
# no aws_ecs_service, no ALB target group, no desired_count.
# Invoke it with `aws ecs run-task`. NOTE: standalone RunTask tasks cannot join
# Service Connect - the RunTask API has no serviceConnectConfiguration parameter,
# it's only settable on aws_ecs_service. So this task can't resolve "mlflow" /
# "fastapi" via Service Connect DNS. Instead its command resolves their current
# private IPs itself via ecs:ListTasks/DescribeTasks (see ecs_resolve_endpoints.py
# and the dvc_task IAM role below) before running dvc repro.

resource "aws_iam_role" "dvc_task" {
  name = "${local.name_prefix}-dvc-task"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "dvc_task_describe_tasks" {
  name = "describe-sibling-tasks"
  role = aws_iam_role.dvc_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "DescribeSiblingTasks"
        Effect   = "Allow"
        Action   = ["ecs:ListTasks", "ecs:DescribeTasks"]
        Resource = "*"
        Condition = {
          ArnEquals = { "ecs:cluster" = aws_ecs_cluster.main.arn }
        }
      }
    ]
  })
}

resource "aws_ecs_task_definition" "dvc" {
  family                   = "${local.name_prefix}-dvc"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.dvc_task.arn # no AWS perms beyond ListTasks/DescribeTasks: MLflow proxies S3 artifact I/O

  container_definitions = jsonencode([
    {
      name      = "dvc"
      image     = "${aws_ecr_repository.repos["dvc"].repository_url}:latest"
      essential = true
      # Only used when the ECS task definition's command override runs (nightly
      # schedule / manual trigger). Dockerfile.train's default CMD (`dvc repro`,
      # used by local docker-compose --profile train) is untouched.
      command = [
        "sh", "-c",
        "eval \"$(python3 ecs_resolve_endpoints.py)\" && dvc repro && curl -sf -X POST \"http://$FASTAPI_HOST:8000/admin/reload\""
      ]
      environment = [
        { name = "ECS_CLUSTER", value = aws_ecs_cluster.main.name },
        { name = "MLFLOW_SERVICE_NAME", value = aws_ecs_service.mlflow.name },
        { name = "FASTAPI_SERVICE_NAME", value = aws_ecs_service.fastapi.name }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs["dvc"].name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "dvc"
        }
      }
    }
  ])
}
