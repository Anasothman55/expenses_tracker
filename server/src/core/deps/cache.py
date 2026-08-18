from fastapi import Request
from redis.asyncio import Redis


def get_redis(req: Request) -> Redis:
  return req.app.state.redis







