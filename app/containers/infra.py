from dependency_injector import containers, providers
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from redis.asyncio import Redis
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

    # Redis
    redis = providers.Singleton(
        Redis.from_url,
        url=config.provided.REDIS_URL,
        decode_responses=True,
    )

    stream_name = providers.Object(settings.REDIS_STREAM_NAME)
    consumer_group = providers.Object(settings.REDIS_CONSUMER_GROUP)
    consumer_name = providers.Object(settings.REDIS_CONSUMER_NAME)

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
        temperature=0.5,
    )

    encoder = providers.Singleton(
        HuggingFaceCrossEncoder,
        model_name="BAAI/bge-reranker-v2-m3",
    )

    re_ranker = providers.Singleton(
        CrossEncoderReranker,
        model=encoder,
        top_n=3,
    )
