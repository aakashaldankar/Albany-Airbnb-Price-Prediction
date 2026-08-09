resource "aws_ecs_task_definition" "gradio" {
  family                   = "${local.name_prefix}-gradio"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([
    {
      name      = "gradio"
      image     = "${aws_ecr_repository.repos["gradio"].repository_url}:latest"
      essential = true
      portMappings = [
        {
          name          = "gradio"
          containerPort = 7860
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "API_URL"
          value = "http://fastapi:8000"
        },
        {
          name  = "GRADIO_SERVER_NAME"
          value = "0.0.0.0"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs["gradio"].name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "gradio"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "gradio" {
  name            = "${local.name_prefix}-gradio"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.gradio.arn
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
      port_name      = "gradio"
      discovery_name = "gradio"
      client_alias {
        port     = 7860
        dns_name = "gradio"
      }
    }
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.gradio.arn
    container_name   = "gradio"
    container_port   = 7860
  }

  depends_on = [aws_lb_listener.gradio]
}