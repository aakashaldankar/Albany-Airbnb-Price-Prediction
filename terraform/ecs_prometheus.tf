resource "aws_ecs_task_definition" "prometheus" {
  family                   = "${local.name_prefix}-prometheus"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([{
    name         = "prometheus"
    image        = "${aws_ecr_repository.repos["prometheus"].repository_url}:latest"
    essential    = true
    portMappings = [{ name = "prometheus", containerPort = 9090, protocol = "tcp" }]
    environment = [
      { name = "FASTAPI_HOST", value = "fastapi" } # Service Connect DNS
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs["prometheus"].name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "prometheus"
      }
    }
  }])
}

resource "aws_ecs_service" "prometheus" {
  name            = "${local.name_prefix}-prometheus"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.prometheus.arn
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
      port_name      = "prometheus"
      discovery_name = "prometheus"
      client_alias {
        port     = 9090
        dns_name = "prometheus" # -> other tasks (Grafana) reach http://prometheus:9090
      }
    }
  }

  # NO load_balancer block -> Prometheus is invisible to the internet, same as FastAPI
}
