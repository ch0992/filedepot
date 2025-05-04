from typing import Any, Optional
from .sentry import capture_exception
import logging
from opentelemetry import trace

class AppException(Exception):
    def __init__(self, code: int, message: str, detail: Any = None, trace_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.detail = detail
        self.trace_id = trace_id or self._get_trace_id()
        super().__init__(message)

    def _get_trace_id(self):
        ctx = trace.get_current_span()
        if ctx and ctx.get_span_context().is_valid:
            return hex(ctx.get_span_context().trace_id)
        return None

def capture_and_log(exc: Exception, logger: logging.Logger = None, extra: dict = None):
    trace_id = None
    ctx = trace.get_current_span()
    if ctx and ctx.get_span_context().is_valid:
        trace_id = hex(ctx.get_span_context().trace_id)
    log_extra = extra or {}
    if trace_id:
        log_extra["trace_id"] = trace_id
    if logger:
        logger.error(f"Exception captured: {exc}", extra=log_extra)
    capture_exception(exc)
    # 추가 확장: span_id 등 context 포함 가능
