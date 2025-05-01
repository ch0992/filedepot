"""
데이터 서비스 API 라우터
"""
from fastapi import APIRouter
from app.data.schemas.sqls import SQLsQueryResponse
from app.data.services.interfaces.meta_query_interface import IMetaQueryService
from app.data.services.impl.meta_query_service import MetaQueryService

router = APIRouter()

@router.get("/imgplt/sqls", tags=["data"], summary="SQL 기반 메타데이터 조회", description="query 파라미터로 전달된 SQL을 실행하여 메타 정보를 반환", response_model=SQLsQueryResponse)
async def get_sqls(query: str, service: IMetaQueryService = MetaQueryService()):
    return await service.query(type('Obj', (), {'query': query})())
