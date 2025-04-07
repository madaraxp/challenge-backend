import boto3

from src.config import settings


def get_aws_client(resource: str):
    client = boto3.client(
        resource,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    return client
