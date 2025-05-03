from typing import List
from app.services.file.services.interfaces.meta_query_interface import MetaQueryInterface
from app.services.file.schemas.sqls import MetaInfoSchema

class MetaQueryService(MetaQueryInterface):
    async def query_metadata(self, query: str) -> List[MetaInfoSchema]:
        # 실제 DB 연동 및 쿼리 실행 로직이 들어가야 함
        # 여기서는 예시로 더미 데이터 반환
        return [
            MetaInfoSchema(id=1, name="meta1", value="value1"),
            MetaInfoSchema(id=2, name="meta2", value="value2")
        ]
