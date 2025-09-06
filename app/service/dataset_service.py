from datetime import datetime, timezone
import uuid

from app.core.config import settings
from app.core.fastapi.transaction import transactional
from app.models.dataset import DatasetEntity
from app.crud.dataset_crud import DatasetCRUD


class DatasetService:
    def __init__(self, s3, crud: DatasetCRUD):
        self.s3 = s3
        self.crud = crud

    async def generate_pre_signed_url(self, file_name: str):

        # key 생성
        date = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        u8 = uuid.uuid4().hex[:8]
        key = f"datasets/{date}/{file_name}/{u8}"

        # pre_signed_url 생성
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": settings.BUCKET,
                    "Key": key,
                },
                ExpiresIn=3600,
            )

        except Exception as e:
            return {"message": "presigned URL 생성 실패", "error": str(e)}

        return {"key": key, "upload_url": url}

    @transactional(commit=True)
    async def confirm_upload(self, key: str):

        head = self.s3.head_object(Bucket=settings.BUCKET, Key=key)

        entity_kwargs = {
            "bucket": settings.BUCKET,
            "object_key": key,
            "filename": key.split("/")[-2],
            "content_type": head.get("ContentType"),
            "size_bytes": head.get("ContentLength"),
            "version_id": head.get("VersionId"),
        }

        entity = DatasetEntity(**entity_kwargs)

        return await self.crud.save(entity)
