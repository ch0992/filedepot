import os
import logging
from typing import Optional
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# Jaeger, Zipkin 등 확장 가능

_otel_exporter = os.getenv("OTEL_EXPORTER", "console")
_service_name = os.getenv("SERVICE_NAME", "filedepot-service")

_tracer_provider = None

def init_tracer(exporter_type: Optional[str] = None):
    global _tracer_provider
    exporter_type = exporter_type or _otel_exporter
    _tracer_provider = TracerProvider(resource=Resource.create({"service.name": _service_name}))
    if exporter_type == "console":
        _tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    elif exporter_type == "otlp":
        _tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    # 확장: Jaeger, Zipkin 등
    trace.set_tracer_provider(_tracer_provider)

# 서비스 main.py 등에서 init_tracer() 호출 필요
init_tracer()

def get_tracer(service_name: Optional[str] = None):
    return trace.get_tracer(service_name or _service_name)

def inject_trace_context(logger, span=None):
    ctx = trace.get_current_span() if span is None else span
    if ctx and ctx.get_span_context().is_valid:
        trace_id = ctx.get_span_context().trace_id
        span_id = ctx.get_span_context().span_id
        return logging.LoggerAdapter(logger, {"trace_id": trace_id, "span_id": span_id})
    return logger
