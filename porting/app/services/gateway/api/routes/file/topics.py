"""
[📄 topics.py - Gateway Route]

설명:
- /topics/{topic} POST API를 처리
- Kafka를 통해 단건 파일 메타데이터를 발행
- 인증 모드(local/remote)에 따라 accessToken 검증 및 권한 체크 수행
- 내부적으로 file_metadata_service.produce_metadata와 await 통신

주요 연동:
- file_metadata_service (Kafka 연동)
- 인증 모듈(auth_service)
"""

from fastapi import APIRouter, Path, status, Header, HTTPException
from app.common.exceptions import BadRequestException, NotFoundException, SystemConfigException
from app.services.gateway.services.impl.file_metadata_service import FileMetadataService
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.core.config import settings
from app.services.log.tracing import get_tracer
from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency, auth_service
from fastapi import Depends
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter()
file_metadata_service = FileMetadataService()
tracer = get_tracer("gateway")

@router.post(
    "/topics/{topic}",
    response_model=KafkaProduceResult,
    tags=["File"],
    summary="Kafka를 통한 메타데이터 적재",
    description="단건 메타 정보를 Kafka topic으로 발행합니다."
)
async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = ...,
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    """
    Kafka를 통해 단건 파일 메타데이터를 발행하는 API

    Args:
        topic (str): Kafka topic명
        body (FileMetadataRequest): 메타데이터 요청 본문
        authorization (Optional[str]): 인증 토큰 (헤더, remote 모드에서 필요)

    Returns:
        KafkaProduceResult: Kafka 발행 결과

    Raises:
        HTTPException: 인증 실패 또는 내부 오류 발생 시
    """
    # WHY: remote 모드에서는 accessToken 검증을 통해 사용자 권한을 확인해야 함
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        # 토큰 유효성 및 권한 체크
        await auth_service.verify_token_and_get_workspaces(access_token)
    # local 모드면 인증 생략
    try:
        # file_metadata_service를 통해 Kafka로 메타데이터 발행
        result = await file_metadata_service.produce_metadata(topic, body)
        return result
    except Exception as e:
        # 예외 발생 시 500 반환
        raise HTTPException(status_code=500, detail=str(e))
