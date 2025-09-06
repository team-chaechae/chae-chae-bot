from dependency_injector import containers, providers

from app.service.dataset_service import DatasetService


class DomainsContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()

    # Service
    dataset_service = providers.Factory(
        DatasetService,
        s3=infra.s3,
    )
