# ---- ALB: the only internet-facing SG ----

resource "aws_security_group" "alb" {
  name   = "${local.name_prefix}-alb-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    description = "Gradio to the world"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "MLflow UI - restricted to you"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr] # least-privilege: only your IP sees MLflow
  }

  ingress {
    description = "Grafana UI - restricted to you"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ---- ECS tasks: allow ALB in on app ports, and allow tasks to talk to each other ----

resource "aws_security_group" "ecs_tasks" {
  name   = "${local.name_prefix}-ecs-tasks-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    description     = "Gradio from ALB"
    from_port       = 7860
    to_port         = 7860
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description     = "MLflow from ALB"
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description     = "Grafana from ALB"
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # No separate rule needed for Grafana -> Prometheus:9090 or Prometheus -> FastAPI:8000 —
  # both already covered by the self-referencing all-ports rule below.
  ingress {
    description = "Service Connect: tasks talk to each other within this SG"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true # any task in this SG can reach any other — simple for dev
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}