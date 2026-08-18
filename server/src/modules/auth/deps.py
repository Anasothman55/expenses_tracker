from typing import Annotated, Sequence, TypedDict

from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.errors.auth import (
  TokenIsMissingException,
  InvalidTokenTypeException,
  UnauthorizedException,
  InActiveUserException)
from src.core.errors.sql import NotFoundException
from src.core.security.jsonwebtoken import jwt_decode, TokenPayload, bearer
from src.core.deps.db import get_db
from src.infrastructure.db.models import UserModel
from src.shared.utils.ctype import ExceptionDetails
from src.shared.utils.model_repository import ModelRepository

class GetTokenType(TypedDict):
  access_token: str
  refresh_token : str


def get_refresh_cookie(
    request: Request,
)-> str:
  refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)

  if not refresh_token:
    raise TokenIsMissingException(
      detail=[ExceptionDetails(
        loc=["cookie", "refresh_token"],
        type="value_error.missing_cookie",
        input=None,
        msg="Refresh token cookie is missing."
      )]
    )

  return refresh_token


def get_optional_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
)-> str | None:
  return credentials.credentials if credentials else None


def get_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]
)-> str:
  if not credentials:
    raise TokenIsMissingException(
      detail=[ExceptionDetails(
        loc=["header", "authorization"],
        type="value_error.missing_header",
        input=None,
        msg="Authorization header not provided."
      )]
    )
  return credentials.credentials


def get_access_token_payload(
    token: Annotated[str, Depends(get_bearer_token)],
)-> TokenPayload:
  decoded = jwt_decode(token)

  if decoded.type != 'access':
    raise InvalidTokenTypeException(
      detail=[ExceptionDetails(
        loc=["header", "authorization"],
        type="value_error.invalid_type",
        input=None,
        msg="Can't use refresh token as access token."
      )]
    )

  return decoded

async def get_current_user(
    payload: Annotated[TokenPayload, Depends(get_access_token_payload)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
  async with ModelRepository[UserModel](db, UserModel) as repo:
    try:
      user = await repo.get_one('uid', payload.sub, )
    except NotFoundException:
      raise UnauthorizedException(detail=[ExceptionDetails(
        loc=["cookie", "access_token"],
        msg="Could not validate credentials",
        type="invalid_credentials",
        input=None,
      )])
    if not user.is_active:
      raise InActiveUserException(
        detail=[ExceptionDetails(
          loc=['body', 'email'],
          msg='This account is currently inactive. Please contact support for assistance.',
          type='type_error.account_inactive',
          input=user.email,
        )]
      )
    return user


