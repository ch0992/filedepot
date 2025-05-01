"""
app/core/exceptions.py
공통 예외 정의
"""

class AppException(Exception):
    """Base application exception"""
    pass

class NotFoundException(AppException):
    pass
