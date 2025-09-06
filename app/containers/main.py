from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector import providers
from app.containers.infra import InfraContainer
from app.containers.domain import DomainsContainer


class MainContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "app.core.fastapi",
            "app.api.v1",
        ]
    )

    infra = providers.Container(InfraContainer)
    domains = providers.Container(DomainsContainer, infra=infra)
