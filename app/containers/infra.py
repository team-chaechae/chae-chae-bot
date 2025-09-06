from dependency_injector import containers, providers
from app.core.config import settings
from app.database.session import AsyncScopedSession
import boto3
from botocore.config import Config as BotoConfig


class InfraContainer(containers.DeclarativeContainer):
    config = providers.Object(settings)

    # DB 세션
    session = providers.Object(AsyncScopedSession)

    # S3
    s3 = providers.Singleton(
        boto3.client,
        "s3",
        endpoint_url=config.provided.MINIO_ENDPOINT,
        aws_access_key_id=config.provided.MINIO_ACCESS_KEY,
        aws_secret_access_key=config.provided.MINIO_SECRET_KEY,
        config=BotoConfig(s3={"addressing_style": "path"}),
        region_name=config.provided.REGION,
    )
