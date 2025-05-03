from typing import Protocol, List
from app.services.file.schemas.sqls import MetaInfoSchema

class FileSqlsInterface(Protocol):
    async def query_metadata(self, query: str) -> List[MetaInfoSchema]:
        ...
