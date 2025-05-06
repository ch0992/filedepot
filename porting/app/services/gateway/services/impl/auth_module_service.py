class AuthService:
    async def verify_token_and_get_workspaces(self, access_token: str):
        # 실제 구현에서는 JWT 검증 및 workspace 정보 반환
        # 여기서는 더미 검증 (예: 토큰이 "valid"면 통과)
        if not access_token or access_token == "invalid":
            raise Exception("Invalid access token")
        return ["default_workspace"]

auth_service = AuthService()

async def verify_access_token_dependency(authorization: str):
    # FastAPI Depends에서 사용할 수 있는 의존성 함수
    if not authorization or not authorization.startswith("Bearer "):
        raise Exception("Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    return await auth_service.verify_token_and_get_workspaces(access_token)
