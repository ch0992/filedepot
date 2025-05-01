"""
JWT 기반 인증 서비스 구현체 예시
"""
from app.services.gateway.services.interfaces.auth import IAuthService, AuthRequest, AuthResponse

class JWTAuthService(IAuthService):
    def verify(self, req: AuthRequest) -> AuthResponse:
        # 실제 JWT 검증 로직은 생략(placeholder)
        if req.token == "valid-token":
            return AuthResponse(valid=True, user_id="user123")
        return AuthResponse(valid=False)
