from app.services.data.services.interfaces.cursor_query_interface import CursorQueryInterface
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

class CursorQueryService(CursorQueryInterface):
    async def cursor_query(self, request: CursorQueryRequest) -> CursorQueryResult:
        # 실제 구현에서는 DB에서 SQL 실행 및 커서 기반 페이징 처리
        # 더미 데이터 예시
        records = [
            {"id": 101, "value": "foo"},
            {"id": 102, "value": "bar"}
        ]
        next_cursor = "eyJpZCI6MTAz..." if records else None
        return CursorQueryResult(records=records, next_cursor=next_cursor)
