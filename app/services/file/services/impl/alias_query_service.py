from app.services.file.services.interfaces.alias_query_interface import AliasQueryInterface
from app.services.file.schemas.aliases import AliasEntry
from typing import List, Any

from app.services.log.tracing import get_tracer

from app.services.log.exceptions import capture_and_log

class AliasQueryService(AliasQueryInterface):
    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        tracer = get_tracer("file")
        with tracer.start_as_current_span("file::get_aliases_for_user"):
            try:
                # 실제 환경에서는 DB 조회, 여기서는 mock 데이터
                # user_info['user'] 등으로 사용자별 분기 가능
                return [
                    AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
                    AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
                ]
            except Exception as e:
                capture_and_log(e)
                raise
