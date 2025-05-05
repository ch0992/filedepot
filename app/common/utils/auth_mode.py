from app.core.config import settings

def get_auth_mode() -> str:
    """
    안전하게 AUTH_MODE를 가져오며, 없거나 예외 발생 시 'local'을 반환합니다.
    """
    try:
        return getattr(settings, "AUTH_MODE", "local") or "local"
    except Exception:
        return "local"
