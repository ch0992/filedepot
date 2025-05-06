from abc import ABC, abstractmethod
from typing import Dict, Any

class TableInsertServiceInterface(ABC):
    """
    비즈니스 계층: 테이블 단건 적재를 담당하는 서비스 추상화
    """
    @abstractmethod
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        pass
