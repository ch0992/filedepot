"""
[📄 list.py - Gateway Route]

설명:
- /imgplt/list/{prefix} GET API를 처리
- S3 prefix 경로에 해당하는 파일 목록을 조회
- 인증 모드(local/remote)에 따라 accessToken 검증 및 권한 체크 수행
- 내부적으로 file 서비스(list_files)와 await 통신

주요 연동:
- file 서비스의 FileServiceClient.list_files (HTTP)
- 인증 모듈(auth_service)

WHY: 
- 인증 모드에 따라 accessToken 검증 및 권한 체크를 수행하여 보안을 강화합니다.
- file 서비스와의 통신을 통해 파일 목록을 조회합니다.
"""

from fastapi import APIRouter, Path, Header, status, HTTPException
from app.common.exceptions import NotFoundException, SystemConfigException, UnauthorizedException
from typing import List, Optional
from app.services.file.schemas.listing import S3FileEntry
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.common.utils.auth_mode import get_auth_mode
from app.core.logging import get_tracer, capture_and_log
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

# WHY: file 서비스 클라이언트를 생성하여 file 서비스와 통신합니다.
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

# WHY: 라우터를 생성하여 API 엔드포인트를 정의합니다.
router = APIRouter()
tracer = get_tracer("gateway::list_files")

@router.get(
    "/imgplt/list/{prefix}",
    tags=["File"],
    summary="S3 prefix 기반 파일 리스트 조회",
    description="S3 버킷 내 지정된 prefix 하위의 파일 목록을 조회합니다.",
    response_model=List[S3FileEntry]
)
@capture_and_log(tracer)
async def list_files(
    prefix: str = Path(..., description="S3 prefix 경로"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    """
    S3 prefix에 해당하는 파일 목록을 반환하는 API

    Args:
        prefix (str): S3 prefix 경로
        authorization (Optional[str]): 인증 토큰 (헤더, remote 모드에서 필요)

    Returns:
        List[S3FileEntry]: S3 파일 목록

    Raises:
        UnauthorizedException: 인증 실패 시
        NotFoundException: 파일 없음
        SystemConfigException: 시스템 환경설정 오류 등
        HTTPException: 기타 FastAPI 예외
    """
    # WHY: remote 모드에서는 accessToken 검증을 통해 사용자 권한을 확인해야 함
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise UnauthorizedException("Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        # 토큰 유효성 및 권한 체크
        await auth_service.verify_token_and_get_workspaces(access_token)

    try:
        # file 서비스에 prefix 파일 목록 요청
        result = await file_client.list_files(prefix)
        return result
    except NotFoundException as e:
        # 파일이 없을 때
        raise
    except SystemConfigException as e:
        # 시스템 환경변수 등 오류
        raise
    except HTTPException as e:
        raise
    except Exception as e:
        # 기타 예외는 시스템 예외로 래핑
        raise SystemConfigException(str(e))
