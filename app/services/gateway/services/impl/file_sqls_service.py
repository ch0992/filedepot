from typing import List
from app.services.gateway.services.interfaces.file_sqls_interface import FileSqlsInterface
from app.services.file.services.interfaces.meta_query_interface import MetaQueryInterface
from app.services.file.services.impl.meta_query_service import MetaQueryService
from app.services.file.schemas.sqls import MetaInfoSchema

class FileSqlsService(FileSqlsInterface):
    def __init__(self):
        self.meta_query_service: MetaQueryInterface = MetaQueryService()

    async def query_metadata(self, query: str) -> List[MetaInfoSchema]:
        return await self.meta_query_service.query_metadata(query)
