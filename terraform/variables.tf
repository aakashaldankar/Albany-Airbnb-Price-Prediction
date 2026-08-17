variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "project_name" {
  type    = string
  default = "albany"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability zones to span"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "db_username" {
  type    = string
  default = "mlflow"
}

variable "ecr_repos" {
  type    = list(string)
  default = ["mlflow", "fastapi", "gradio", "dvc", "prometheus", "grafana"]
}

variable "my_ip_cidr" {
  description = "Your public IP in CIDR form, e.g 49.36.x.x/32 - locks down MLflow UI"
  type        = string
}

