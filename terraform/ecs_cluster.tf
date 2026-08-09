resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"
  setting {
    name  = "containerInsights"
    value = "disabled" # dev: keep off to avoid CloudWatch charges. Turn on in Phase B.
  }
}

# Service Connect needs a Cloud Map namespace. This is the "DNS" for internal service names.

resource "aws_service_discovery_http_namespace" "main" {
  name = local.name_prefix # services become reachable as http://:
}