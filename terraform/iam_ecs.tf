data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# ---- Execution role: used by the ECS agent (pull image, fetch secrets, write logs) ----

resource "aws_iam_role" "ecs_execution" {
  name               = "${local.name_prefix}-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "ecs_execution_base" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# The base policy covers ECR + logs, but NOT Secrets Manager. Add it explicitly.

resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "read-secrets"
  role = aws_iam_role.ecs_execution.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["secretsmanager:GetSecretValue"]
      Resource = [
        aws_secretsmanager_secret.backend_store_uri.arn,
        aws_secretsmanager_secret.db_password.arn
      ]
    }]
  })
}

# ---- Task role for MLflow: needs read/write to the artifact bucket ----

resource "aws_iam_role" "mlflow_task" {
  name               = "${local.name_prefix}-mlflow-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy" "mlflow_s3" {
  name = "mlflow-s3"
  role = aws_iam_role.mlflow_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"]
      Resource = [
        aws_s3_bucket.mlflow_artifacts.arn,
        "${aws_s3_bucket.mlflow_artifacts.arn}/*"
      ]
    }]
  })
}

# ---- Task role for FastAPI/Gradio: no AWS perms needed (MLflow proxies artifacts) ----

resource "aws_iam_role" "app_task" {
  name               = "${local.name_prefix}-app-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}