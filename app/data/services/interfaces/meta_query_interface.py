from abc import ABC, abstractmethod
from app.data.schemas.sqls import SQLsQueryRequest, SQLsQueryResponse

class IMetaQueryService(ABC):
    @abstractmethod
    async def query(self, req: SQLsQueryRequest) -> SQLsQueryResponse:
        pass
