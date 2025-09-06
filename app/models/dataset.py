from dataclasses import dataclass
import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String, func

from app.database.base import Base


class DatasetORM(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    bucket = Column(String, nullable=False)
    object_key = Column(String, nullable=False, unique=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    version_id = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)


@dataclass(kw_only=True)
class DatasetEntity:
    id: Optional[int] = None
    bucket: str
    object_key: str
    filename: str
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None
    version_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


def to_entity(row: DatasetORM) -> DatasetEntity:
    return DatasetEntity(
        id=row.id,
        bucket=row.bucket,
        object_key=row.object_key,
        filename=row.filename,
        content_type=row.content_type,
        size_bytes=row.size_bytes,
        version_id=row.version_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
    )


def to_orm(entity: DatasetEntity) -> DatasetORM:
    return DatasetORM(
        bucket=entity.bucket,
        object_key=entity.object_key,
        filename=entity.filename,
        content_type=entity.content_type,
        size_bytes=entity.size_bytes,
        version_id=entity.version_id,
        deleted_at=entity.deleted_at,
    )
