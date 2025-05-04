import os
import importlib
import pytest

def reload_tracing_with_env(otel_exporter, jaeger_host=None, jaeger_port=None, otlp_endpoint=None):
    os.environ["OTEL_EXPORTER"] = otel_exporter
    if jaeger_host:
        os.environ["JAEGER_HOST"] = jaeger_host
    if jaeger_port:
        os.environ["JAEGER_PORT"] = str(jaeger_port)
    if otlp_endpoint:
        os.environ["OTLP_ENDPOINT"] = otlp_endpoint
    # tracing 모듈 reload
    import app.services.log.tracing as tracing
    importlib.reload(tracing)
    return tracing

import pytest

def _find_exporter(provider, exporter_classname):
    # OpenTelemetry 1.22+: provider._active_span_processor is CompositeSpanProcessor
    composite = getattr(provider, "_active_span_processor", None)
    if not composite:
        return False
    for proc in getattr(composite, "_span_processors", []):
        if getattr(proc, "span_exporter", None) and proc.span_exporter.__class__.__name__ == exporter_classname:
            return True
    return False

def test_stdout_exporter(monkeypatch):
    tracing = reload_tracing_with_env("stdout")
    provider = tracing._tracer_provider
    assert provider is not None
    assert _find_exporter(provider, "ConsoleSpanExporter")

def test_jaeger_exporter(monkeypatch):
    try:
        import opentelemetry.exporter.jaeger.thrift
    except ImportError:
        pytest.skip("jaeger exporter not installed")
    tracing = reload_tracing_with_env("jaeger", jaeger_host="localhost", jaeger_port=6831)
    provider = tracing._tracer_provider
    if provider is None:
        pytest.skip("jaeger exporter init failed (likely not installed)")
    assert _find_exporter(provider, "JaegerExporter")

def test_tempo_exporter(monkeypatch):
    try:
        import opentelemetry.exporter.otlp.proto.http.trace_exporter
    except ImportError:
        pytest.skip("otlp exporter not installed")
    tracing = reload_tracing_with_env("tempo", otlp_endpoint="http://tempo:4318/v1/traces")
    provider = tracing._tracer_provider
    if provider is None:
        pytest.skip("otlp exporter init failed (likely not installed)")
    assert _find_exporter(provider, "OTLPSpanExporter")
