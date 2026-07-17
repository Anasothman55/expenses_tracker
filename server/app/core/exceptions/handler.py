from typing import Any, Sequence
from fastapi import status, Request, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.shared.schema.error_response import ErrorResponse


class AppException(Exception):
  status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
  message: str  = 'An unexpected error occurred'
  error_code: str = 'INTERNAL_SERVER_ERROR'

  def __init__(
    self,
    message: str | None = None,
    detail: Sequence[Any] | None = None,
    delete_cookies: list[str] | None = None
  ):
    self.message = message or self.message
    self.detail = detail  # extra context (e.g. which field failed)
    self.delete_cookies = delete_cookies or []
    super().__init__(self.message)



async def app_exception_handler(request: Request, exc: AppException):
  res = JSONResponse(
    status_code=exc.status_code,
    content=jsonable_encoder(ErrorResponse(
      status_code=exc.status_code,
      message=exc.message,
      detail=exc.detail,
      error_code=exc.error_code,
    ).model_dump())
  )
  for cookie in exc.delete_cookies:
    res.delete_cookie(cookie)
  return res

async def validation_exception_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
    status_code=422,
    content=ErrorResponse(
      status_code=422,
      error_code='UNPROCESSABLE_CONTENT',
      message='Request validation failed.',
      detail=exc.errors()
    ).model_dump()
  )


async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content=ErrorResponse(
      status_code=exc.status_code,
      error_code="HTTP_ERROR",
      message=str(exc.detail),
      detail=jsonable_encoder(exc.detail),
    ).model_dump(),
  )




