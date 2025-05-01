from app.data.services.interfaces.meta_query_interface import IMetaQueryService
from app.data.schemas.sqls import SQLsQueryRequest, SQLsQueryResponse, Metadata

class MetaQueryService(IMetaQueryService):
    async def query(self, req: SQLsQueryRequest) -> SQLsQueryResponse:
        # mock: query 파라미터에 따라 결과 다르게 반환
        if not req.query or 'fail' in req.query.lower():
            return SQLsQueryResponse(items=[])
        # 예시: 쿼리 결과 mock
        items = [
            Metadata(column="id", type="int", sample=1),
            Metadata(column="name", type="str", sample="abc")
        ]
        return SQLsQueryResponse(items=items)
