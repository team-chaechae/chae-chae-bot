from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    REGION: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_ENDPOINT: str
    BUCKET: str
    CHROMA_DIR: str

    class Config:
        env_file = ".env"


settings = Config()