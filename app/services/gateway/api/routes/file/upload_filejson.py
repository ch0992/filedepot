from fastapi import APIRouter, UploadFile, File, Path, Header, HTTPException, status, Depends, Body, Form
from typing import Optional
from app.services.gateway.services.interfaces.file_upload_interface import FileUploadInterface
from app.common.utils.auth_mode import get_auth_mode
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.services.file.schemas.upload import UploadResponse
from app.services.file.schemas.metadata import FileMetadataRequest
import json

router = APIRouter()

@router.post(
    "/file-json/{topic}",
    tags=["file"],
    summary="파일+메타데이터(JSON) 업로드 및 Kafka 발행",
    description="S3에 파일 업로드 후, JSON 형식의 메타데이터를 multipart/form-data로 받아 Kafka topic으로 발행.",
    response_model=UploadResponse
)
async def upload_file_and_metadata_json(
    topic: str = Path(..., description="Kafka topic 이름"),
    file: UploadFile = File(..., description="업로드할 파일"),
    metadata: str = Form(..., description="JSON 형식의 메타데이터 문자열 예시: {\"file_id\":\"abc123\",\"filename\":\"test.png\",\"owner\":\"user1\",\"size\":12345}"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
    service: FileUploadInterface = FileUploadInterface.get_service()
    return await service.upload_file_and_metadata_json(topic, file, metadata)
