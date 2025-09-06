from datetime import datetime, timezone
import uuid

from app.core.config import settings


class DatasetService:
    def __init__(self, s3):
        self.s3 = s3

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