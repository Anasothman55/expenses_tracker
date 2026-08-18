from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import Request

from time import time, perf_counter
from rich import print
from loguru import logger
import uuid

# not in use
async def logger_middleware(req: Request, call_next):
  start_time = time()

  res = await call_next(req)
  end_time = time()
  log_dict = {
    'url': str(req.url.path),
    'method': str(req.method),
    'status': str(res.status_code),
    'process_time': str(end_time - start_time),
  }

  logger.info(log_dict)
  return res



class LoggerMiddleware:
  def __init__(self, app: ASGIApp) -> None:
    self.app = app

  async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    if scope['type'] != 'http':
      await self.app(scope, receive, send)
      return

    request_id = str(uuid.uuid4())
    req = Request(scope, receive)
    start = perf_counter()
    status_code = 0

    async def send_wrapper(message):
      nonlocal status_code
      if message["type"] == "http.response.start":
        status_code = message["status"]
      await send(message)

    with logger.contextualize(
      request_id=request_id,
      method=req.method,
      path=req.url.path,
    ):
      try:
        await self.app(scope, receive, send_wrapper)
      except Exception:
        logger.exception("Unhandled exception")
        raise
      finally:
        duration = perf_counter() - start
        logger.info({
          'url': str(req.url.path),
          'method': str(req.method),
          'status': str(status_code),
          'process_time': f'({duration:.6f}s)',
        })













