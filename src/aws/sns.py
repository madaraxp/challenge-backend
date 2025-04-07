from odmantic import ObjectId

from src.aws.client import get_aws_client
from src.config import settings

sns_client = get_aws_client('sns')


def publish_topic(owner_id: ObjectId):
    sns_client.publish(
        TopicArn=settings.SNS_TOPIC_CATALOG_ARN,
        Message=str(owner_id),
        MessageStructure='string',
    )
