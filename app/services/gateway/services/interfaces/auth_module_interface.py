from abc import ABC, abstractmethod
from app.services.gateway.schemas.auths import AuthWorkspaceList

class AuthModuleInterface(ABC):
    @abstractmethod
    async def verify_token_and_get_workspaces(self, access_token: str) -> AuthWorkspaceList:
        pass
