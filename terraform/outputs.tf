output "vpc_id" { value = module.vpc.vpc_id }
output "public_subnet_ids" { value = module.vpc.public_subnets }
output "private_subnet_ids" { value = module.vpc.private_subnets }
output "ecr_repo_urls" { value = { for k, v in aws_ecr_repository.repos : k => v.repository_url } }
output "mlflow_bucket_name" { value = aws_s3_bucket.mlflow_artifacts.bucket }
output "rds_endpoint" { value = aws_db_instance.mlflow.endpoint }
output "rds_password_secret" { value = aws_secretsmanager_secret.db_password.name }
output "alb_dns_name" { value = aws_lb.main.dns_name }
output "gradio_url" { value = "http://${aws_lb.main.dns_name}" }
output "mlflow_url" { value = "http://${aws_lb.main.dns_name}:5000" }
