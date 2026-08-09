resource "aws_cloudwatch_log_group" "ecs" {
  for_each          = toset(["mlflow", "fastapi", "gradio"])
  name              = "/ecs/${local.name_prefix}/${each.value}"
  retention_in_days = 7
}