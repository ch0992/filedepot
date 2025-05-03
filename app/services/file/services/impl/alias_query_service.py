from app.services.file.services.interfaces.alias_query_interface import AliasQueryInterface
from app.services.file.schemas.aliases import AliasEntry
from typing import List, Any

class AliasQueryService(AliasQueryInterface):
    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        # 실제 환경에서는 DB 조회, 여기서는 mock 데이터
        # user_info['user'] 등으로 사용자별 분기 가능
        return [
            AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
            AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
        ]
