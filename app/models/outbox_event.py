from dataclasses import dataclass
import datetime
from typing import Optional
from sqlalchemy import JSON, Column, DateTime, Integer, String, func
from app.database.base import Base


class OutboxEventORM(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True)
    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


@dataclass(kw_only=True)
class OutboxEventEntity:
    id: Optional[int] = None
    aggregate_type: str
    aggregate_id: int
    event_type: str
    payload: dict
    status: str = "PENDING"
    created_at: Optional[datetime] = None


def to_entity(row: OutboxEventORM) -> OutboxEventEntity:
    return OutboxEventEntity(
        id=row.id,
        aggregate_type=row.aggregate_type,
        aggregate_id=row.aggregate_id,
        event_type=row.event_type,
        payload=row.payload,
        status=row.status,
        created_at=row.created_at,
    )


def to_orm(entity: OutboxEventEntity) -> OutboxEventORM:
    return OutboxEventORM(
        aggregate_type=entity.aggregate_type,
        aggregate_id=entity.aggregate_id,
        event_type=entity.event_type,
        payload=entity.payload,
        status=entity.status,
    )
