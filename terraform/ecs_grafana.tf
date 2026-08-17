resource "aws_ecs_task_definition" "grafana" {
  family                   = "${local.name_prefix}-grafana"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([{
    name         = "grafana"
    image        = "${aws_ecr_repository.repos["grafana"].repository_url}:latest"
    essential    = true
    portMappings = [{ name = "grafana", containerPort = 3000, protocol = "tcp" }]
    environment = [
      { name = "PROMETHEUS_HOST", value = "prometheus" }, # Service Connect DNS
      { name = "GF_SECURITY_ADMIN_USER", value = "admin" }
    ]
    secrets = [
      { name = "GF_SECURITY_ADMIN_PASSWORD", valueFrom = aws_secretsmanager_secret.grafana_admin_password.arn }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs["grafana"].name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "grafana"
      }
    }
  }])
}

resource "aws_ecs_service" "grafana" {
  name            = "${local.name_prefix}-grafana"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.grafana.arn
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
      port_name      = "grafana"
      discovery_name = "grafana"
      client_alias {
        port     = 3000
        dns_name = "grafana"
      }
    }
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.grafana.arn
    container_name   = "grafana"
    container_port   = 3000
  }

  depends_on = [aws_lb_listener.grafana, aws_ecs_service.prometheus]
}
