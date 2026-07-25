terraform {
  required_version = ">=1.9.0"

  backend "s3" {
    bucket         = "albany-tfstate-aakash-1784974762"
    key            = "albany-airbnb/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "albany-tfstate-lock"
    encrypt        = true
  }

  required_providers {
    aws    = { source = "hashicorp/aws", version = "~>5.60" }
    random = { source = "hashicorp/random", version = "~>3.6" }
  }
}