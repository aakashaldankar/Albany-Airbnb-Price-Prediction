resource "aws_db_subnet_group" "mlflow" {
  name       = "${local.name_prefix}-mlflow-db-subnets"
  subnet_ids = module.vpc.private_subnets # RDS lives in private subnets - never public 
}

resource "aws_security_group" "rds" {
  name        = "${local.name_prefix}-rds-sg"
  description = "Postgres access from within VPC"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr] # only VPC-internal traffic. ECS tasks reach it; internet cannot.
    description = "Postgres from VPC"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "mlflow" {
  identifier        = "${local.name_prefix}-mlflow-db"
  engine            = "postgres"
  engine_version    = "16.14"
  instance_class    = "db.t4g.micro" # free tier eligible
  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "mlflow"
  username = var.db_username
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.mlflow.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false # never true

  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false

  apply_immediately = true
}