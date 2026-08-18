from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination

from slowapi import _rate_limit_exceeded_handler # type: ignore
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware

from src.core.config import settings
from src.core.errors.handler import (
  AppException,
  app_exception_handler,
  validation_exception_handler,
  http_exception_handler
)
from src.core.lifespan import fastapi_lifespan
from src.core.middleware.logger_middleware import LoggerMiddleware
from src.modules.routes import router_v1
from src.shared.schema.main import HealthCheckResponse
from src.core.limiter import limiter

app = FastAPI(
  title='Expenses API',
  version='0.1.0',

  contact={
    "name": 'Anas Othman',
    "email": 'anasothman581@gmail.com',
  },

  lifespan=fastapi_lifespan,
  docs_url= '/docs' if settings.DEVELOP_MODE else None,
  redoc_url= '/redoc' if settings.DEVELOP_MODE else None,
  openapi_url= '/openapi.json' if settings.DEVELOP_MODE else None,
)

#add_pagination(app)


app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# Add middleware
#app.add_middleware(BaseHTTPMiddleware, dispatch=logger_middleware)
app.add_middleware(LoggerMiddleware)
app.add_middleware(SlowAPIASGIMiddleware)

# Add routes
app.include_router(router_v1, prefix='/api')

@app.get('/health', status_code=status.HTTP_200_OK, response_model=HealthCheckResponse)
@limiter.limit("10/minute")
async def index(request: Request) -> HealthCheckResponse:
  return HealthCheckResponse(
    health=True,
    status='Ok',
    message='Expenses API',
  )

