from fastapi import APIRouter, Depends, File, UploadFile, status
from dependency_injector.wiring import inject, Provide

from app.schemas.dataset import PresignedUrlResponse
from app.service.dataset_service import DatasetService

router = APIRouter(
    prefix="/v1/datasets",
    tags=["datasets"],
)


@router.post(
    "/upload",
    summary="MinIO presigned URL 발급",
    description="클라이언트가 직접 MinIO 에 파일을 업로드하기 전에, presigned URL을 발급받습니다.",
    response_model=PresignedUrlResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def generate_pre_signed_url(
    file: UploadFile = File(...),
    service: DatasetService = Depends(Provide["domains.dataset_service"]),
):
    result = await service.generate_pre_signed_url(file.filename)
    return PresignedUrlResponse(**result)
