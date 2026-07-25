provider "aws" {
  region  = var.aws_region
  profile = "albany"

  default_tags {
    tags = {
      Project     = "albany-airbnb"
      Environment = var.environment
      ManagedBy   = "terraform"
      Owner       = "aakash"
    }
  }
}