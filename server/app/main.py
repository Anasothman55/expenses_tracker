from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError


from slowapi import _rate_limit_exceeded_handler # type: ignore
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware

from app.core.config import settings
from app.core.exceptions.handler import (
  AppException,
  app_exception_handler,
  validation_exception_handler,
  http_exception_handler
)
from app.core.lifespan import fastapi_lifespan
from app.core.middleware.logger_middleware import LoggerMiddleware
from app.modules.routes import router_v1
from app.shared.schema.main import HealthCheckResponse
from app.core.limiter import limiter

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



# Add exception handler
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middleware
#app.add_middleware(BaseHTTPMiddleware, dispatch=logger_middleware)
app.add_middleware(LoggerMiddleware)
app.add_middleware(SlowAPIASGIMiddleware)

# Add routes
app.include_router(router_v1, prefix='/api')

@app.get('/', status_code=status.HTTP_200_OK, response_model=HealthCheckResponse)
@limiter.limit("10/minute")
async def index(request: Request) -> HealthCheckResponse:
  return HealthCheckResponse(
    health=True,
    status='Ok',
    message='Expenses API',
  ).model_dump()

