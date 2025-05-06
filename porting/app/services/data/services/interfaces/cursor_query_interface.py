from abc import ABC, abstractmethod
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

class CursorQueryInterface(ABC):
    @abstractmethod
    async def cursor_query(self, request: CursorQueryRequest) -> CursorQueryResult:
        pass
