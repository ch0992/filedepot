"""
[📄 upload.py - 파일 업로드 API 라우터]

설명:
- 파일 업로드 관련 엔드포인트 제공
- 인증된 사용자만 접근 가능

주요 연동:
- FileUploadInterface (서비스)
- get_auth_mode (의존성)
"""

from fastapi import APIRouter, UploadFile, File, Form, Path, Header, HTTPException, status, Depends
from typing import Optional
from app.services.gateway.services.interfaces.file_upload_interface import FileUploadInterface
from app.common.utils.auth_mode import get_auth_mode
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.services.file.schemas.upload import UploadResponse

router = APIRouter()

# 기존 upload_file_and_metadata 엔드포인트는 분리된 새로운 엔드포인트로 대체됨
from fastapi import APIRouter
from .upload_filemeta import router as file_meta_router
from .upload_filejson import router as file_json_router

router = APIRouter()

# /upload/file-meta (파일+메타데이터 파일)
router.include_router(file_meta_router, prefix="/upload")
# /upload/file-json (파일+메타데이터 JSON)
router.include_router(file_json_router, prefix="/upload")

# 필요시 추가 endpoint/라우터를 여기에 등록
