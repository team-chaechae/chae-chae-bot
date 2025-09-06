from dependency_injector import containers, providers
from app.core.config import settings
from app.database.session import AsyncScopedSession
import boto3
from botocore.config import Config as BotoConfig

from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama


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

    # Embeddings
    embeddings = providers.Singleton(
        HuggingFaceEmbeddings,
        model_name="BAAI/bge-m3",
        encode_kwargs={"normalize_embeddings": True},
    )

    # Chroma
    chroma_settings = providers.Object(
        ChromaSettings(
            anonymized_telemetry=False,
            allow_reset=False,
        )
    )

    chroma = providers.Singleton(
        Chroma,
        collection_name="cosine_collection",
        embedding_function=embeddings,
        persist_directory=config.provided.CHROMA_DIR,
        client_settings=chroma_settings,
        collection_metadata={"hnsw:space": "cosine"},
    )

    llm = providers.Singleton(
        ChatOllama,
        model="exaone3.5",
        temperature=0.3,
    )
