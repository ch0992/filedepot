from abc import ABC, abstractmethod
from typing import List, Any
from app.services.file.schemas.aliases import AliasEntry

class AliasQueryInterface(ABC):
    @abstractmethod
    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        pass
