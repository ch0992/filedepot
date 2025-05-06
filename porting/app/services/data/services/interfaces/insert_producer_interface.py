from abc import ABC, abstractmethod
from typing import Dict, Any

class InsertProducerInterface(ABC):
    @abstractmethod
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        pass
