from dependency_injector import containers, providers

from app.crud.dataset_crud import DatasetCRUD
from app.service.dataset_service import DatasetService


class DomainsContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()

    # Repositorie
    dataset_crud = providers.Factory(
        DatasetCRUD,
        session=infra.session,
    )

    # Service
    dataset_service = providers.Factory(
        DatasetService,
        s3=infra.s3,
        crud=dataset_crud,
    )
