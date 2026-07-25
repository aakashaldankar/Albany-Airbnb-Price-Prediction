resource "random_id" "suffix" {
  byte_length = 4 # make bucket name globally unique
}

resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket        = "${local.name_prefix}-mlflow-artifacts-${random_id.suffix.hex}"
  force_destroy = true # so 'terraform destroy' doesn't fail on non-empty bucket (dev only!)
}

resource "aws_s3_bucket_versioning" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_public_access_block" "mlflow_artifacts" {
  bucket                  = aws_s3_bucket.mlflow_artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

