from pydantic import BaseModel
from typing import Any, Dict

class InsertPayload(BaseModel):
    __root__: Dict[str, Any]

    def dict(self, *args, **kwargs):
        return self.__root__
