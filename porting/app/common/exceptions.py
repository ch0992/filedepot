from fastapi import HTTPException, status

class BadRequestException(HTTPException):
    def __init__(self, detail="잘못된 요청입니다."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail="인증이 필요합니다."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail="권한이 없습니다."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail="리소스를 찾을 수 없습니다."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(HTTPException):
    def __init__(self, detail="이미 존재합니다."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnprocessableEntityException(HTTPException):
    """
    요청 처리 불가 예외

    - HTTP 상태 코드: 422
    - 예외 메시지: 요청을 처리할 수 없습니다.
    """
    def __init__(self, detail="요청을 처리할 수 없습니다."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class SystemConfigException(HTTPException):
    """
    시스템 환경설정 예외

    - HTTP 상태 코드: 500
    - 예외 메시지: 시스템 환경설정 오류입니다. 운영자에게 문의하세요.
    """
    def __init__(self, detail="시스템 환경설정 오류입니다. 운영자에게 문의하세요."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ServiceUnavailableException(HTTPException):
    """
    서비스 사용 불가 예외

    - HTTP 상태 코드: 503
    - 예외 메시지: 서비스를 사용할 수 없습니다.
    """
    def __init__(self, detail="서비스를 사용할 수 없습니다."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
