"""
[📄 upload_filejson.py - Gateway Route]

설명:
- /file-json/{topic} POST API를 처리
- 파일과 JSON 메타데이터를 multipart/form-data로 받아 S3 업로드 및 Kafka 발행
- 인증 모드(local/remote)에 따라 accessToken 검증 및 권한 체크 수행
- 내부적으로 FileUploadInterface.upload_file_and_metadata_json 호출

주요 연동:
- FileUploadInterface (파일 업로드 및 Kafka 연동)
- 인증 모듈(auth_service)
"""

from fastapi import APIRouter, UploadFile, File, Path, Header, status, Depends, Body, Form, HTTPException
from app.common.exceptions import BadRequestException, NotFoundException, SystemConfigException
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
    tags=["File"],
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
    """
    파일과 JSON 메타데이터를 함께 업로드하고 Kafka로 발행하는 API

    Args:
        topic (str): Kafka topic 이름
        file (UploadFile): 업로드할 파일
        metadata (str): JSON 형식의 메타데이터 문자열
        authorization (Optional[str]): 인증 토큰 (헤더, remote 모드에서 필요)

    Returns:
        UploadResponse: 업로드 및 Kafka 발행 결과

    Raises:
        HTTPException: 인증 실패 또는 내부 오류 발생 시
    """
    # WHY: remote 모드에서는 accessToken 검증을 통해 사용자 권한을 확인해야 함
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        # 토큰 유효성 및 권한 체크
        await auth_service.verify_token_and_get_workspaces(access_token)
    service: FileUploadInterface = FileUploadInterface.get_service()
    # WHY: 파일과 메타데이터를 동시에 업로드 후 Kafka로 발행해야 데이터 일관성 보장
    return await service.upload_file_and_metadata_json(topic, file, metadata)
