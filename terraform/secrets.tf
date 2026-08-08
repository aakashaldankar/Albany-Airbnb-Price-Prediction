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