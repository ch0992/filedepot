from fastapi import APIRouter, Query, Depends
from app.data.schemas.sqls import SQLsQueryResponse
from app.data.services.interfaces.meta_query_interface import IMetaQueryService
from app.data.services.impl.meta_query_service import MetaQueryService
from typing import Annotated

router = APIRouter()

@router.get(
    "/imgplt/sqls",
    tags=["data"],
    summary="SQL 기반 메타데이터 조회",
    description="query 파라미터로 전달된 SQL을 실행하여 메타 정보를 반환",
    response_model=SQLsQueryResponse
)
async def get_sqls(
    query: Annotated[str, Query(..., description="실행할 SQL 쿼리")],
    service: IMetaQueryService = Depends(MetaQueryService)
):
    from app.data.schemas.sqls import SQLsQueryRequest
    req = SQLsQueryRequest(query=query)
    return await service.query(req)
