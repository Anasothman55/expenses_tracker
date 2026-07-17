import logging
import sys
from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
  """Redirect all stdlib logging records into loguru."""

  def emit(self, record: logging.LogRecord) -> None:
    # Map stdlib level name → loguru level
    try:
      level = logger.level(record.levelname).name
    except ValueError:
      level = record.levelno

    # Find the actual caller (skip loguru internals)
    frame, depth = logging.currentframe(), 2
    while frame.f_code.co_filename == logging.__file__:
      frame = frame.f_back
      depth += 1

    logger.opt(depth=depth, exception=record.exc_info).log(
      level, record.getMessage()
    )


def setup_logging(log_level: settings.LOG_LEVEL, json_logs: settings.LOG_JSON) -> None:
  # Remove loguru's default handler
  logger.remove()
  logging.getLogger("uvicorn.access").handlers = []
  logging.getLogger("uvicorn.access").propagate = False
  # Add your preferred sink
  logger.add(
    sys.stdout,
    level=log_level,
    serialize=json_logs,   # True → JSON output for production
    backtrace=True,
    diagnose=not json_logs,  # disable in prod (can expose sensitive values)
    enqueue=True,            # async-safe, important with uvicorn workers
  )

  # Optional: also write to file
  logger.add(
    "logs/app.log",
    rotation="100 MB",
    compression="zip",
    level="TRACE",
    serialize=json_logs,
    enqueue=True,
  )

  # Redirect all stdlib loggers (uvicorn, fastapi, sqlalchemy, etc.) → loguru
  logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

  for name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
    logging.getLogger(name).handlers = [InterceptHandler()]


