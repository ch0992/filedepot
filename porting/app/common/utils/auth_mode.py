from app.core.config import settings

"""
[📄 auth_mode.py - Auth Mode Utility]

설명:
- 인증 모드(예: 개발, 운영 등)를 반환하는 유틸리티 함수
- 환경 변수 또는 기본값 활용
"""

def get_auth_mode() -> str:
    """
    안전하게 AUTH_MODE를 가져오며, 없거나 예외 발생 시 'local'을 반환합니다.
    """
    try:
        return getattr(settings, "AUTH_MODE", "local") or "local"
    except Exception:
        return "local"
