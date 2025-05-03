from app.services.gateway.services.interfaces.file_alias_interface import FileAliasInterface
from app.services.file.services.impl.alias_query_service import AliasQueryService
from app.services.file.schemas.aliases import AliasEntry
from typing import List, Any

class FileAliasService(FileAliasInterface):
    def __init__(self):
        self.query_service = AliasQueryService()

    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        # user_info에서 user_id 등 필요한 정보 추출 (예: user_info['user'] 등)
        return await self.query_service.get_aliases(user_info)
