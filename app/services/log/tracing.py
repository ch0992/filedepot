import os
import logging
from typing import Optional
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
try:
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
except ImportError:
    JaegerExporter = None
# Jaeger, Zipkin 등 확장 가능

_otel_exporter = os.getenv("OTEL_EXPORTER", "stdout")
_service_name = os.getenv("SERVICE_NAME", "filedepot-service")

_tracer_provider = None

def init_tracer(exporter_type: Optional[str] = None):
    global _tracer_provider
    try:
        exporter_type = (exporter_type or _otel_exporter or "stdout").lower()
        if exporter_type == "none":
            # 익스포터 등록하지 않음 (테스트 환경 등)
            return
        _tracer_provider = TracerProvider(resource=Resource.create({"service.name": _service_name}))
        exporter = None
        if exporter_type in ("console", "stdout"):
            exporter = ConsoleSpanExporter()
        elif exporter_type == "jaeger":
            if not JaegerExporter:
                raise ImportError("opentelemetry-exporter-jaeger-thrift not installed")
            jaeger_host = os.getenv("JAEGER_HOST", "localhost")
            jaeger_port = int(os.getenv("JAEGER_PORT", 6831))
            exporter = JaegerExporter(agent_host_name=jaeger_host, agent_port=jaeger_port)
        elif exporter_type in ("tempo", "otlp"):
            otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://tempo:4318/v1/traces")
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        else:
            exporter = ConsoleSpanExporter()
        _tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(_tracer_provider)
    except Exception as e:
        logging.warning(f"[Tracing fallback] tracer init failed: {e}")
        _tracer_provider = None

# 서비스 main.py 등에서 init_tracer() 호출 필요
try:
    init_tracer()
except Exception as e:
    logging.warning(f"[Tracing fallback] global tracer init failed: {e}")

def get_tracer(service_name: Optional[str] = None):
    try:
        tracer_provider = trace.get_tracer_provider()
        tracer = tracer_provider.get_tracer(service_name or _service_name)
        if tracer is None:
            raise RuntimeError("Tracer is None")
        return tracer
    except Exception as e:
        logging.warning(f"[Tracing fallback] tracer unavailable: {e}")
        class NoOpTracer:
            def start_as_current_span(self, *args, **kwargs):
                from contextlib import nullcontext
                return nullcontext()
        return NoOpTracer()

# --- 글로벌 로그 포맷터 패치: 모든 로그에 trace_id/ span_id 자동 포함 ---
class TraceIdFormatter(logging.Formatter):
    def format(self, record):
        # trace_id, span_id가 없는 경우에도 항상 필드가 출력되도록 보장
        if not hasattr(record, "trace_id"):
            record.trace_id = self._get_trace_id()
        if not hasattr(record, "span_id"):
            record.span_id = self._get_span_id()
        return super().format(record)
    def _get_trace_id(self):
        span = trace.get_current_span()
        if span and span.get_span_context().is_valid:
            return format(span.get_span_context().trace_id, 'x')
        return "-"
    def _get_span_id(self):
        span = trace.get_current_span()
        if span and span.get_span_context().is_valid:
            return format(span.get_span_context().span_id, 'x')
        return "-"

# 모든 핸들러에 TraceIdFormatter 적용
def patch_global_logging_format():
    fmt = "%(levelname)s %(trace_id)s %(span_id)s %(name)s:%(lineno)d %(message)s"
    trace_fmt = TraceIdFormatter(fmt)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(trace_fmt)
    # uvicorn, filedepot 등 주요 로거에도 적용
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "filedepot"]:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.setFormatter(trace_fmt)

patch_global_logging_format()


def inject_trace_context(logger, span=None):
    ctx = trace.get_current_span() if span is None else span
    if ctx and ctx.get_span_context().is_valid:
        trace_id = ctx.get_span_context().trace_id
        span_id = ctx.get_span_context().span_id
        return logging.LoggerAdapter(logger, {"trace_id": format(trace_id, 'x'), "span_id": format(span_id, 'x')})
    return logger
