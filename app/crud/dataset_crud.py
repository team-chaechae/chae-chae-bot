from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dataset import DatasetEntity, to_entity, to_orm


class DatasetCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: DatasetEntity) -> DatasetEntity:
        orm = to_orm(entity)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        return to_entity(orm)
