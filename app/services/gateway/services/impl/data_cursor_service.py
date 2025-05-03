from app.services.gateway.services.interfaces.data_cursor_interface import DataCursorInterface
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult
from app.services.data.services.impl.cursor_query_service import CursorQueryService

class DataCursorService(DataCursorInterface):
    def __init__(self):
        self.cursor_query_service = CursorQueryService()

    async def cursor_query(self, request: CursorQueryRequest) -> CursorQueryResult:
        return await self.cursor_query_service.cursor_query(request)
