from pydantic import BaseModel
from typing import List

class AuthWorkspaceList(BaseModel):
    workspaces: List[str]
    valid: bool = True
