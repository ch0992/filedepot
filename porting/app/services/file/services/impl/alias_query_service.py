"""
[📄 alias_query_service.py - File 서비스 구현체]

설명:
- 파일 alias 목록 조회 서비스 구현체
- 인증된 사용자 ID 기반 alias 목록 반환

주요 연동:
- AliasQueryInterface (인터페이스)
- AliasEntry (스키마)
"""

from app.services.file.services.interfaces.alias_query_interface import AliasQueryInterface
from app.services.file.schemas.aliases import AliasEntry
from typing import List, Any

from app.services.log.tracing import get_tracer

from app.services.log.exceptions import capture_and_log

class AliasQueryService(AliasQueryInterface):
    """
    파일 alias 목록 조회 서비스 구현체
    """
    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        """
        인증된 사용자 ID로 접근 가능한 alias 목록 반환
        Args:
            user_info (Any): 사용자 정보
        Returns:
            List[AliasEntry]: alias 목록
        """
        # WHY: 사용자별 접근 가능한 alias만 반환해야 함
        # WHY: 트레이싱을 위해 tracer를 초기화
        tracer = get_tracer("file")
        with tracer.start_as_current_span("file::get_aliases_for_user"):
            try:
                # WHY: 실제 환경에서는 DB 조회, 여기서는 mock 데이터
                # WHY: 사용자별 분기 로직 추가 필요
                # user_info['user'] 등으로 사용자별 분기 가능
                return [
                    AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
                    AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
                ]
            except Exception as e:
                capture_and_log(e)
                raise
