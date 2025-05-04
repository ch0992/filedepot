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

def capture_and_log(exc: Exception, span, logger: logging.Logger = None, extra: dict = None):
    try:
        trace_id = None
        try:
            ctx = trace.get_current_span()
            if ctx and ctx.get_span_context().is_valid:
                trace_id = hex(ctx.get_span_context().trace_id)
        except Exception as e:
            if logger:
                logger.warning(f"[capture_and_log] trace context unavailable: {e}")
        log_extra = extra or {}
        if trace_id:
            log_extra["trace_id"] = trace_id
        if logger:
            try:
                logger.error(f"Exception captured: {exc}", extra=log_extra)
            except Exception as e:
                print(f"[capture_and_log] logger error: {e}")
        try:
            capture_exception(exc)
        except Exception as e:
            if logger:
                logger.warning(f"[capture_and_log] sentry capture failed: {e}")
        if span is not None:
            if RECORD_EXCEPTION_EVENT:
                span.record_exception(exc)
            if SET_SPAN_ERROR_STATUS:
                span.set_status(StatusCode.ERROR)
    except Exception as e:
        print(f"[capture_and_log] fallback error: {e}")
