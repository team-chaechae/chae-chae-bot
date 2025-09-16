from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox_event import OutboxEventEntity, OutboxEventORM, to_entity, to_orm


class OutboxCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: OutboxEventEntity) -> OutboxEventEntity:
        orm = to_orm(entity)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        return to_entity(orm)

    async def claim_pending(
        self, limit: int
    ) -> list[OutboxEventEntity]:

        stmt = (
            select(OutboxEventORM)
            .where(OutboxEventORM.status == "PENDING")
            .order_by(OutboxEventORM.created_at.asc(), OutboxEventORM.id.asc())
            .with_for_update(skip_locked=True)
            .limit(limit)
        )

        orms = (await self.session.scalars(stmt)).all()
        for orm in orms:
            orm.status = "SENDING"

        return [to_entity(o) for o in orms]

    async def mark_sent(self, ids: List[int]) -> None:
        if not ids:
            return

        stmt = (
            update(OutboxEventORM)
            .where(OutboxEventORM.id.in_(ids), OutboxEventORM.status == "SENDING")
            .values(status="SENT")
            .execution_options(synchronize_session=False)
        )

        await self.session.execute(stmt)

    async def mark_complete(self, id: int) -> None:
        if not id:
            return

        stmt = (
            update(OutboxEventORM)
            .where(OutboxEventORM.id == id, OutboxEventORM.status == "SENT")
            .values(status="COMPLETE")
            .execution_options(synchronize_session=False)
        )

        await self.session.execute(stmt)
