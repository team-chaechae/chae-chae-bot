from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    REGION: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_ENDPOINT: str
    BUCKET: str
    CHROMA_DIR: str
    REDIS_URL: str
    REDIS_STREAM_NAME: str
    REDIS_CONSUMER_GROUP: str
    REDIS_CONSUMER_NAME: str
    OUTBOX_PUBLISH_BATCH: int
    OUTBOX_POLL_INTERVAL_MS: int

    class Config:
        env_file = ".env"


settings = Config()