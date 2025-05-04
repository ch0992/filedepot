from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .exceptions import AppException, capture_and_log
from .tracing import get_tracer, inject_trace_context
import logging
import traceback

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
