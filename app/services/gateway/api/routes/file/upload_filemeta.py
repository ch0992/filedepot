from fastapi import APIRouter, UploadFile, File, Path, Header, HTTPException, status, Depends
from typing import Optional
from app.services.gateway.services.interfaces.file_upload_interface import FileUploadInterface
from app.common.utils.auth_mode import get_auth_mode
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.services.file.schemas.upload import UploadResponse

router = APIRouter()

@router.post(
    "/file-meta/{topic}",
    tags=["file"],
    summary="파일+메타데이터 파일 업로드 및 Kafka 발행",
    description="S3에 파일과 JSON 메타데이터 파일을 함께 업로드 후, 메타데이터를 Kafka topic으로 발행.",
    response_model=UploadResponse
)
async def upload_file_and_metadata_file(
    topic: str = Path(..., description="Kafka topic 이름"),
    file: UploadFile = File(..., description="업로드할 파일"),
    metadata_file: UploadFile = File(..., description="JSON 메타데이터 파일 업로드 (application/json)"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
    service: FileUploadInterface = FileUploadInterface.get_service()
    return await service.upload_file_and_metadata_file(topic, file, metadata_file)
