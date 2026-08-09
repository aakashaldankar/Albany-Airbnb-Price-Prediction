resource "aws_lb" "main" {
  name               = "${local.name_prefix}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
}

# ----- Gradio target group + listener on :80 -----

resource "aws_lb_target_group" "gradio" {
  name        = "${local.name_prefix}-gradio-tg"
  port        = 7860
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip" # Fargate = awsvpc = IP targets
  health_check {
    path                = "/"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    timeout             = 5
    interval            = 30
    matcher             = "200-399"
  }
}

resource "aws_lb_listener" "gradio" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.gradio.arn
  }
}

# ----- MLflow target group + listener on :5000 (your IP only, via ALB SG) -----

resource "aws_lb_target_group" "mlflow" {
  name        = "${local.name_prefix}-mlflow-tg"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"
  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    timeout             = 5
    interval            = 30
    matcher             = "200-399"
  }
}

resource "aws_lb_listener" "mlflow" {
  load_balancer_arn = aws_lb.main.arn
  port              = 5000
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.mlflow.arn
  }
}