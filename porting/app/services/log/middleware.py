from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .exceptions import AppException, capture_and_log
from .tracing import get_tracer, inject_trace_context
import logging
import traceback
import os

ENABLE_HTTP_EXCEPTION_TRACE = os.getenv("ENABLE_HTTP_EXCEPTION_TRACE", "true").lower() == "true"
CUSTOM_HTTP_EXCEPTION_HANDLER = os.getenv("CUSTOM_HTTP_EXCEPTION_HANDLER", "true").lower() == "true"
SENTRY_CAPTURE_HTTP_EXCEPTION = os.getenv("SENTRY_CAPTURE_HTTP_EXCEPTION", "false").lower() == "true"

class TraceLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tracer = get_tracer()
        with tracer.start_as_current_span(f"HTTP {request.method} {request.url.path}") as span:
            logger = logging.getLogger("filedepot")
            logger = inject_trace_context(logger, span)
            trace_ctx = span.get_span_context()
            logger.info(
                f"[access] {request.method} {request.url.path}",
                extra={
                    "path": str(request.url),
                    "trace_id": format(trace_ctx.trace_id, 'x') if trace_ctx and trace_ctx.is_valid else "-",
                    "span_id": format(trace_ctx.span_id, 'x') if trace_ctx and trace_ctx.is_valid else "-"
                }
            )
            try:
                response = await call_next(request)
                return response
            except Exception as exc:
                capture_and_log(exc, logger, extra={"path": str(request.url)})
                raise

def install_exception_handlers(app: FastAPI):
    if CUSTOM_HTTP_EXCEPTION_HANDLER:
        @app.exception_handler(HTTPException)
        async def custom_http_exception_handler(request: Request, exc: HTTPException):
            # OpenTelemetry trace 연동
            if ENABLE_HTTP_EXCEPTION_TRACE:
                try:
                    from opentelemetry import trace
                    span = trace.get_current_span()
                    if span is not None:
                        span.set_attribute("http.status_code", exc.status_code)
                        span.set_attribute("http.exception.detail", str(exc.detail))
                        span.set_status(trace.status.Status(trace.status.StatusCode.ERROR, str(exc.detail)))
                except Exception:
                    pass
            # Sentry 연동
            if SENTRY_CAPTURE_HTTP_EXCEPTION:
                try:
                    import sentry_sdk
                    sentry_sdk.capture_exception(exc)
                except Exception:
                    pass
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger = logging.getLogger("filedepot")
        logger = inject_trace_context(logger)
        logger.error(f"AppException: {exc.message}", extra={"trace_id": getattr(exc, "trace_id", None)})
        return JSONResponse(status_code=exc.code, content={"error": exc.message, "detail": exc.detail, "trace_id": exc.trace_id})

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger = logging.getLogger("filedepot")
        logger = inject_trace_context(logger)
        logger.error(f"Unhandled Exception: {exc}")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
