module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~>5.13"

  name = "${local.name_prefix}-vpc"
  cidr = var.vpc_cidr

  azs             = var.azs
  public_subnets  = local.public_subnets
  private_subnets = local.private_subnets

  enable_nat_gateway = true
  single_nat_gateway = true # cost-saver: 1 NAT instead of 2 (~$32/mo saved)
  # trade-off: if that AZ dies, private subnets lose internet
  # totally fine for dev/portfolio

  enable_dns_hostnames = true
  enable_dns_support   = true

  # tag subnets so ECS/ALB can discover them via tags later
  public_subnet_tags  = { Tier = "public" }
  private_subnet_tags = { Tier = "private" }
}