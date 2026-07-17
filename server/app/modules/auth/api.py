from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request, status
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps.db import get_db
from app.core.deps.cache import get_redis
from .deps import get_refresh_cookie, get_optional_bearer_token
from .schema import (
  UserRegisterSchema,
  UserRegisterResponseSchema,
  UserVerifyResponseSchema,
  UserLoginSchema,
  UserLoginResponseSchema,
  UserRefreshTokenResponseSchema,
  UserForgotPasswordResponseSchema,
  UserForgotPasswordSchema,
  UserResetPasswordVerifyResponseSchema,
  UserResetPasswordVerifySchema,
  UserChangePasswordResponseSchema,
  UserChangePasswordSchema
)
from .service import (
  register_service,
  verify_service,
  login_service,
  refresh_service,
  logout_service,
  forgot_password_service,
  reset_password_verify_service,
  change_password_service
)
from app.core.limiter import limiter

auth_route = APIRouter(
  tags=['Auth'],
)


@auth_route.post('/register', response_model=UserRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register(
    request: Request,
    body: UserRegisterSchema,
    db: Annotated[AsyncSession,Depends(get_db)]
):
  return await register_service(body=body, db=db)

@auth_route.get('/verify/{verify_token}', response_model=UserVerifyResponseSchema, status_code=status.HTTP_200_OK)
@limiter.limit("10/hour")
async def verify(
    request: Request,
    verify_token: str,
    db: Annotated[AsyncSession,Depends(get_db)]
):
  return await verify_service(verify_token=verify_token, db=db)

@auth_route.post('/login',response_model=UserLoginResponseSchema,  status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
@limiter.limit("20/hour")
async def login(
    request: Request,
    body: UserLoginSchema,
    db: Annotated[AsyncSession,Depends(get_db)],
    redis_conn: Annotated[Redis, Depends(get_redis)],
    res: Response
):
  return await login_service(db, redis_conn, body, res)


@auth_route.get('/refresh-token', response_model=UserRefreshTokenResponseSchema,  status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def refresh_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
    response: Response,
    redis_conn: Annotated[Redis, Depends(get_redis)],
    refresh_tokens: Annotated[str, Depends(get_refresh_cookie)],
    access_token: Annotated[str | None, Depends(get_optional_bearer_token)],
):
  return await refresh_service(db, response, redis_conn, refresh_tokens, access_token)

@auth_route.get('/logout')
async def logout(
    refresh_tokens: Annotated[str, Depends(get_refresh_cookie)],
    redis_conn: Annotated[Redis, Depends(get_redis)],
    response: Response,
):
  return await logout_service(refresh_tokens, redis_conn, response)

@auth_route.post('/forgot-password', response_model=UserForgotPasswordResponseSchema, status_code=status.HTTP_200_OK)
@limiter.limit("5/hour")
async def forgot_password(
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
    redis_conn: Annotated[Redis, Depends(get_redis)],
    body: UserForgotPasswordSchema
):
  return await forgot_password_service(db, body,redis_conn)

@auth_route.post('/reset-password-verify', response_model=UserResetPasswordVerifyResponseSchema, status_code=status.HTTP_200_OK)
@limiter.limit("10/10minutes")
async def reset_password_verify(
    request: Request,
    redis_conn: Annotated[Redis, Depends(get_redis)],
    body: UserResetPasswordVerifySchema
):
  return await reset_password_verify_service(body, redis_conn)

@auth_route.put('/reset-password', response_model=UserChangePasswordResponseSchema, status_code=status.HTTP_200_OK)
@limiter.limit("5/10minutes")
async def change_password(
    request: Request,
    redis_conn: Annotated[Redis, Depends(get_redis)],
    body: UserChangePasswordSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
):
  return await change_password_service(body, redis_conn, db)





