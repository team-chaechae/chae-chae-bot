from dependency_injector import containers, providers

from app.core.config import settings
from app.database.session import AsyncScopedSession


class InfraContainer(containers.DeclarativeContainer):
    config = providers.Object(settings)

    # DB 세션 
    session = providers.Object(AsyncScopedSession)