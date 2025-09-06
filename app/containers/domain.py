from dependency_injector import containers, providers

class DomainsContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()