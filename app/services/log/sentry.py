import os
import sentry_sdk

_sentry_dsn = os.getenv("SENTRY_DSN", None)
_sentry_env = os.getenv("ENV", "development")

_sentry_inited = False

def init_sentry(dsn: str = None, environment: str = None):
    global _sentry_inited
    dsn = dsn or _sentry_dsn
    environment = environment or _sentry_env
    if dsn and not _sentry_inited:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=1.0,
            environment=environment,
        )
        _sentry_inited = True

def capture_exception(exc: Exception):
    if _sentry_dsn:
        sentry_sdk.capture_exception(exc)
