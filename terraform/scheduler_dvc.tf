# Nightly retrain trigger, independent of GitHub Actions - this keeps firing
# regardless of the TRAIN_NOW flag in .github/workflows/deploy.yml.

resource "aws_iam_role" "scheduler_dvc" {
  name = "${local.name_prefix}-scheduler-dvc"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "scheduler.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "scheduler_dvc_run_task" {
  name = "run-dvc-task"
  role = aws_iam_role.scheduler_dvc.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "RunDvcTask"
        Effect   = "Allow"
        Action   = "ecs:RunTask"
        Resource = "${aws_ecs_task_definition.dvc.arn_without_revision}:*"
        Condition = {
          ArnEquals = { "ecs:cluster" = aws_ecs_cluster.main.arn }
        }
      },
      {
        Sid    = "PassDvcRoles"
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = [
          aws_iam_role.ecs_execution.arn,
          aws_iam_role.dvc_task.arn
        ]
      }
    ]
  })
}

resource "aws_scheduler_schedule" "dvc_nightly_retrain" {
  name                = "${local.name_prefix}-dvc-nightly-retrain"
  schedule_expression = "cron(0 2 * * ? *)"
  # EventBridge Scheduler evaluates the cron in this timezone directly - no
  # manual UTC conversion needed for "2am every morning, IST".
  schedule_expression_timezone = "Asia/Kolkata"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_ecs_cluster.main.arn
    role_arn = aws_iam_role.scheduler_dvc.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.dvc.arn
      launch_type         = "FARGATE"

      network_configuration {
        subnets          = module.vpc.private_subnets
        security_groups  = [aws_security_group.ecs_tasks.id]
        assign_public_ip = false
      }
    }
  }
}
