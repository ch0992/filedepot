"""
기본 로그 수집 서비스 구현체 예시
"""
from app.services.log.services.interfaces.log_collect import ILogCollectService, LogCollectRequest, LogCollectResponse

class BasicLogCollectService(ILogCollectService):
    def collect(self, req: LogCollectRequest) -> LogCollectResponse:
        # 실제 로그 수집 로직은 생략(placeholder)
        logs = [f"log from {req.start_time} to {req.end_time}"]
        return LogCollectResponse(logs=logs)
