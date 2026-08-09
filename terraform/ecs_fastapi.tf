resource "aws_ecs_task_definition" "fastapi" {
  family                   = "${local.name_prefix}-fastapi"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([{
    name         = "fastapi"
    image        = "${aws_ecr_repository.repos["fastapi"].repository_url}:latest"
    essential    = true
    portMappings = [{ name = "fastapi", containerPort = 8000, protocol = "tcp" }]
    environment = [
      { name = "MLFLOW_TRACKING_URI", value = "http://mlflow:5000" }, # Service Connect DNS
      { name = "MODEL_NAME", value = "albany-price-predictor" },
      { name = "MODEL_ALIAS", value = "champion" }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs["fastapi"].name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "fastapi"
      }
    }
  }])
}

resource "aws_ecs_service" "fastapi" {
  name            = "${local.name_prefix}-fastapi"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  # exposes "fastapi" to Gradio AND (by being in the namespace) can reach "mlflow"

  service_connect_configuration {
    enabled   = true
    namespace = aws_service_discovery_http_namespace.main.arn
    service {
      port_name      = "fastapi"
      discovery_name = "fastapi"
      client_alias {
        port     = 8000
        dns_name = "fastapi"
      }
    }
  }

  # NO load_balancer block -> FastAPI is invisible to the internet
}