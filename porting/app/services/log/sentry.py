import os
import sentry_sdk

_sentry_dsn = os.getenv("SENTRY_DSN", None)
_sentry_env = os.getenv("ENV", "development")

_sentry_inited = False

import logging

def init_sentry(dsn: str = None, environment: str = None):
    global _sentry_inited
    dsn = dsn or _sentry_dsn
    environment = environment or _sentry_env
    if not dsn:
        logging.warning("[Sentry fallback] SENTRY_DSN 미설정, Sentry 비활성화")
        return
    if not _sentry_inited:
        try:
            sentry_sdk.init(
                dsn=dsn,
                traces_sample_rate=1.0,
                environment=environment,
            )
            _sentry_inited = True
        except Exception as e:
            logging.warning(f"[Sentry fallback] sentry init failed: {e}")

def capture_exception(exc: Exception):
    if not _sentry_dsn:
        logging.warning(f"[Sentry fallback] SENTRY_DSN 미설정, 예외만 출력: {exc}")
        return
    try:
        sentry_sdk.capture_exception(exc)
    except Exception as e:
        logging.warning(f"[Sentry fallback] sentry capture_exception failed: {e}")
