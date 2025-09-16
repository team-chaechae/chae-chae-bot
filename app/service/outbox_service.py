from app.core.fastapi.transaction import transactional
from app.crud.outbox_crud import OutboxCRUD
from app.models.outbox_event import OutboxEventEntity


class OutboxService:
    def __init__(self, outbox_crud: OutboxCRUD):
        self.outbox_crud = outbox_crud

    async def create_outbox(
        self, aggregate_type: str, aggregate_id: int, event_type: str, payload: dict
    ):
        outbox_entity = OutboxEventEntity(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload
        )

        await self.outbox_crud.save(outbox_entity)
        
    @transactional(commit=True)
    async def claim_pending(self, limit: int):
        return await self.outbox_crud.claim_pending(limit)

    @transactional(commit=True)
    async def mark_sent(self, id_list):
        if not id_list:
            return
        await self.outbox_crud.mark_sent(id_list)

    @transactional(commit=True)
    async def mark_complete(self, id):
        if not id:
            return
        await self.outbox_crud.mark_complete(id)
