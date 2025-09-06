from dependency_injector import containers, providers

from app.core.config import settings


class InfraContainer(containers.DeclarativeContainer):
    config = providers.Object(settings)