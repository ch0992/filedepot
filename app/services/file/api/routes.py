"""
파일 서비스 API 라우터
"""
from fastapi import APIRouter, Query
from app.services.file.schemas.aliases import AliasEntry
from typing import List

router = APIRouter()

@router.get("/ping", summary="Ping-pong API")
async def ping():
    return {"message": "pong"}

@router.get("/aliases", response_model=List[AliasEntry], summary="사용자별 적재 alias 목록 조회")
async def aliases(user_id: str = Query(...)):
    # 실제로는 DB 등에서 user_id별 alias 조회
    return [
        AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
        AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
    ]
