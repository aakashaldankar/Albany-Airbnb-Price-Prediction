# DVC training job. This is a batch/one-off task, not a long-running service:
# no aws_ecs_service, no ALB target group, no desired_count.
# Invoke it with `aws ecs run-task` (see terraform_architecture.md / plan notes for the command),
# passing a --service-connect-configuration override at run time so the task can
# resolve the internal "mlflow" DNS name - Service Connect client config lives on
# the run-task call for standalone tasks, not on the task definition itself.

resource "aws_ecs_task_definition" "dvc" {
  family                   = "${local.name_prefix}-dvc"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn # no AWS perms needed: MLflow proxies S3 artifact I/O

  container_definitions = jsonencode([
    {
      name      = "dvc"
      image     = "${aws_ecr_repository.repos["dvc"].repository_url}:latest"
      essential = true
      environment = [
        {
          name  = "MLFLOW_TRACKING_URI"
          value = "http://mlflow:5000" # Service Connect DNS - internal only, not the ALB
        }
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
