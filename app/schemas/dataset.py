from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class PresignedUrlResponse(BaseModel):
    key: str = Field(..., description="업로드될 객체 키")
    upload_url: AnyHttpUrl = Field(..., description="MinIO로 PUT할 URL")

    model_config = ConfigDict(from_attributes=True)