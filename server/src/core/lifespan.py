from contextlib import asynccontextmanager

from fastapi import FastAPI

from loguru import logger

from src.core.config import settings
from src.core.loggin import setup_logging
from src.infrastructure.db.engine import db_init, close_db
from src.infrastructure.redis.instanse import redis_conn
from src.core.limiter import limiter

@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
  # Startup
  try:
    setup_logging(log_level=settings.LOG_LEVEL, json_logs=False)

    await db_init()

    app.state.redis = redis_conn
    await app.state.redis.ping()

    app.state.limiter = limiter

    logger.info("Database initialized")
    logger.info("Redis initialized")
    logger.info(f"The server run on: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")

  except Exception as e:
    logger.error(f"Error during startup: {e}")
    raise

  yield

  # Shutdown
  try:
    await close_db()

    await app.state.redis.aclose()

    logger.info("Database closed")
    logger.info("Redis closed")

  except Exception as e:
    logger.error(f"Error during shutdown: {e}")
    raise