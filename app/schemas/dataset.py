from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class PresignedUrlResponse(BaseModel):
    key: str = Field(..., description="업로드될 객체 키")
    upload_url: AnyHttpUrl = Field(..., description="MinIO로 PUT할 URL")

    model_config = ConfigDict(from_attributes=True)

class IngestCallbackRequest(BaseModel):
    key: str = Field(..., description="업로드될 객체 키")

class DatasetResponse(BaseModel):
    id: int
    bucket: str
    object_key: str
    filename: str
    content_type: str | None = None
    size_bytes: int | None = None
    version_id: str | None = None

    model_config = ConfigDict(from_attributes=True)