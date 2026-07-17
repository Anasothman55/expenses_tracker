from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


limiter = Limiter(
  key_func=get_remote_address,
  default_limits=settings.DEFAULT_LIMITER,
  storage_uri=settings.redis_url(),  # or pass storage= directly
)








