import os
import httpx
from fastapi import HTTPException, status, Header, Depends

from app.services.gateway.services.interfaces.auth_module_interface import AuthModuleInterface
from app.services.gateway.schemas.auths import AuthWorkspaceList

import os
import httpx
from fastapi import HTTPException, status, Header, Depends
from app.services.gateway.services.interfaces.auth_module_interface import AuthModuleInterface
from app.services.gateway.schemas.auths import AuthWorkspaceList

AUTH_MODE = os.environ.get("AUTH_MODE", "remote").lower()  # default remote
AUTH_SERVER_URL = os.environ.get("AUTH_SERVER_URL", "http://workspace/auth/verify")

class AuthModuleService(AuthModuleInterface):
    """
    인증 모듈 서비스
    - AUTH_MODE=local: 어떤 토큰이든 인증 성공 (테스트/로컬 개발)
    - AUTH_MODE=remote: AUTH_SERVER_URL로 토큰 검증 (운영)
    """
    async def verify_token(self, token: str) -> dict:
        mode = os.environ.get("AUTH_MODE", "remote").lower()
        print("[auth_service] AUTH_MODE in verify_token:", mode)
        if mode == "local":
            print("[auth_service] LOCAL 인증 우회 성공")
            # 어떤 토큰이든 무조건 인증 성공
            return {"user": "dev", "roles": ["admin"]}
        elif mode == "remote":
            print("[auth_service] REMOTE 인증 서버 호출")
            url = os.environ.get("AUTH_SERVER_URL", "http://workspace/auth/verify")
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                try:
                    resp = await client.get(url, headers=headers, timeout=5)
                except Exception as e:
                    raise HTTPException(status_code=502, detail=f"Auth server unreachable: {str(e)}")
                if resp.status_code == 200:
                    return resp.json()
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid remote access token")
        else:
            print("[auth_service] Invalid AUTH_MODE setting")
            raise HTTPException(status_code=500, detail="Invalid AUTH_MODE setting")

    async def verify_token_and_get_workspaces(self, access_token: str) -> AuthWorkspaceList:
        # 기존 인터페이스 호환: 인증 성공 시 AuthWorkspaceList 반환
        data = await self.verify_token(access_token)
        # 아래는 예시: 실제 workspace 정보는 인증 서버 응답에 따라 다를 수 있음
        workspaces = data.get("workspaces") or ["default-workspace"]
        return AuthWorkspaceList(workspaces=workspaces, valid=True)

auth_service = AuthModuleService()

async def verify_access_token_dependency(authorization: str = Header(..., description="Bearer accessToken")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    await auth_service.verify_token_and_get_workspaces(access_token)

