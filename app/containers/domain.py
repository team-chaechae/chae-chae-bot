from dependency_injector import containers, providers

from app.crud.dataset_crud import DatasetCRUD
from app.crud.outbox_crud import OutboxCRUD
from app.rag.chain import build_rag_chain
from app.service.dataset_service import DatasetService
from app.service.outbox_service import OutboxService
from app.service.streams.indexer import StreamIndexer
from app.service.streams.redis_stream import RedisStream


class DomainsContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()

    # Repositorie
    dataset_crud = providers.Factory(
        DatasetCRUD,
        session=infra.session,
    )

    outbox_crud = providers.Factory(
        OutboxCRUD,
        session=infra.session,
    )

    # Service
    outbox_service = providers.Factory(
        OutboxService,
        outbox_crud=outbox_crud,
    )

    dataset_service = providers.Factory(
        DatasetService,
        s3=infra.s3,
        dataset_crud=dataset_crud,
        outbox_service=outbox_service,
        vectorstore=infra.chroma,
    )

    # RAG Chain
    rag_chain = providers.Singleton(
        build_rag_chain,
        vectorstore=infra.chroma,
        llm=infra.llm,
        re_ranker=infra.re_ranker
    )

    # Reids-Stream
    redis_stream = providers.Factory(
        RedisStream,
        redis=infra.redis,
    )
    
    stream_indexer = providers.Factory(
        StreamIndexer,
        outbox_service=outbox_service,
        stream=redis_stream,
        s3=infra.s3,
        vectorstore=infra.chroma,
    )