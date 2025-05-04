from fastapi import APIRouter, HTTPException, Body, Header, status
from typing import Optional
from app.services.data.services.interfaces.sql_query_interface import SqlQueryInterface
from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log

router = APIRouter()
sql_query_service = SqlQueryInterface()  # 실제 구현체로 대체 필요

@router.post(
    "/imgplt/sqls",
    tags=["data"],
    summary="SQL 실행 결과 조회",
    description="임의 SQL을 실행하고 결과를 반환합니다."
)
async def get_sql_result(
    sql: str = Body(..., embed=True),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    from app.services.log.tracing import get_tracer
    from app.services.log.exceptions import capture_and_log
    import logging
    tracer = get_tracer("gateway-sqls")
    with tracer.start_as_current_span("gateway::sqls") as span:
        try:
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
            # 내부 서비스 호출 시에도 tracing 활용 가능
            result = await sql_query_service.query_by_sql(sql)
            return result
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail="Internal error")
