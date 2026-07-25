locals {
  name_prefix = "${var.project_name}-${var.environment}"

  # split the /16 into four /20s: 2 public + 2 private
  public_subnets  = ["10.0.0.0/20", "10.0.16.0/20"]
  private_subnets = ["10.0.32.0/20", "10.0.48.0/20"]
}