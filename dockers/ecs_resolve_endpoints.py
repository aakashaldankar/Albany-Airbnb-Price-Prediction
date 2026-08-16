"""Resolves mlflow/fastapi private IPs via the ECS API and prints export
statements for `eval`. Standalone ECS tasks (RunTask) can't join Service
Connect - only aws_ecs_service can - so this is how the retrain task finds
its sibling services.
"""

import os
import boto3


def get_task_private_ip(client, cluster: str, service_name: str) -> str:

    task_arns = client.list_tasks(
        cluster=cluster, serviceName=service_name, desiredStatus="RUNNING"
    )["taskArns"]

    if not task_arns:
        raise RuntimeError(f"no running tasks for service {service_name}")

    task = client.describe_tasks(cluster=cluster, tasks=[task_arns[0]])["tasks"][0]

    for detail in task["attachments"][0]["details"]:
        if detail["name"] == "privateIPv4Address":
            return detail["value"]

    raise RuntimeError(f"no private IP found for {service_name}")


def main():

    cluster = os.environ["ECS_CLUSTER"]
    client = boto3.client("ecs")

    mlflow_ip = get_task_private_ip(client, cluster, os.environ["MLFLOW_SERVICE_NAME"])
    fastapi_ip = get_task_private_ip(client, cluster, os.environ["FASTAPI_SERVICE_NAME"])

    print(f"export MLFLOW_TRACKING_URI=http://{mlflow_ip}:5000")
    print(f"export FASTAPI_HOST={fastapi_ip}")


if __name__ == "__main__":
    main()
