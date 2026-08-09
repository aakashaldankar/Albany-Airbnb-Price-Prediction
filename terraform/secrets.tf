resource "random_password" "db" {
  length  = 24
  special = true
  # RDS Postgres disallows these characters in master password 
  override_special = "!*-_"
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${local.name_prefix}/rds/mlflow-password"
  recovery_window_in_days = 0 # dev immediate delete on destroy 
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

resource "aws_secretsmanager_secret" "backend_store_uri" {
  name                    = "${local.name_prefix}/mlflow/backend-store-uri"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "backend_store_uri" {
  secret_id     = aws_secretsmanager_secret.backend_store_uri.id
  secret_string = "postgresql://${var.db_username}:${random_password.db.result}@${aws_db_instance.mlflow.endpoint}/mlflow"
}

