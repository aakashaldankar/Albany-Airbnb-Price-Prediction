resource "aws_ecs_task_definition" "mlflow" {
  family                   = "${local.name_prefix}-mlflow"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.mlflow_task.arn

  container_definitions = jsonencode([{
    name         = "mlflow"
    image        = "${aws_ecr_repository.repos["mlflow"].repository_url}:latest"
    essential    = true
    portMappings = [{ name = "mlflow", containerPort = 5000, protocol = "tcp" }]
    environment = [
      # real S3 -> NO MLFLOW_S3_ENDPOINT_URL here (that was the MinIO-only override)
      { name = "ARTIFACTS_DESTINATION", value = "s3://${aws_s3_bucket.mlflow_artifacts.bucket}/" }
    ]
    secrets = [
      { name = "BACKEND_STORE_URI", valueFrom = aws_secretsmanager_secret.backend_store_uri.arn }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs["mlflow"].name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "mlflow"
      }
    }
  }])
}

resource "aws_ecs_service" "mlflow" {
  name            = "${local.name_prefix}-mlflow"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.mlflow.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  service_connect_configuration {
    enabled   = true
    namespace = aws_service_discovery_http_namespace.main.arn
    service {
      port_name      = "mlflow"
      discovery_name = "mlflow"
      client_alias {
        port     = 5000
        dns_name = "mlflow" # -> other tasks reach http://mlflow:5000
      }
    }
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.mlflow.arn
    container_name   = "mlflow"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener.mlflow]
}