import json
from datetime import timedelta
from uuid import UUID, uuid7
import secrets

from fastapi import Response
from loguru import logger

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.config import settings
from app.core.exceptions.auth import (
  RegistrationConflictException,
  InvalidCredentialsException,
  InActiveUserException,
  EmailNotVerifiedException,
  InvalidTokenException,
  RefreshTokenBlacklistedException,
  InvalidTokenSessionIdException,
  ExpiredTokenException,
  TokenReusedException,
  InvalidResetIdException,
  InvalidOtpException,
  ExpiredPasswordResetTokenException,
  InvalidPasswordResetTokenException,
  SamePasswordException
)
from app.core.exceptions.sql import NotFoundException
from app.core.security.email_reset_password import otp_decoded, OtpData, otp_verify
from app.core.security.email_verify_token import email_verify_token_decoded, email_verify_token_encoded
from app.core.security.jsonwebtoken import  create_access_token, create_refresh_token, jwt_decode
from app.core.security.password_hashing import password_verify, password_hash
from app.core.tasks.email_tasks import send_verify_email_task, send_password_reset_email_task
from app.infrastructure.db.models.users import UserModel
from app.modules.auth.schema import (
  UserRegisterSchema,
  UserRegisterResponseSchema,
  UserVerifyResponseSchema,
  UserLoginSchema,
  UserLoginResponseSchema,
  UserRefreshTokenResponseSchema,
  UserForgotPasswordSchema, UserResetPasswordVerifySchema, UserResetPasswordVerifyResponseSchema,
  UserForgotPasswordResponseSchema, UserChangePasswordSchema, UserChangePasswordResponseSchema
)
from app.shared.utils.api_tree import api_tree
from app.shared.utils.constant import PROJECT_DATETIME
from app.shared.utils.ctype import ExceptionDetails
from app.shared.utils.model_repository import ModelRepository

async def register_service(
  body: UserRegisterSchema,
  db: AsyncSession,
) ->  UserRegisterResponseSchema:
  async with ModelRepository[UserModel](db, UserModel) as repo:

    stmt = (
      select(UserModel)
      .where(
        or_(
          UserModel.email == body.email,
          UserModel.username == body.username,
        )
      )
    )

    exist = await repo.get_all(
      is_pagination= False,
      include_deleted= False,
      params= None,
      select_stmt=stmt,
    )

    if exist:
      conflict_error = []

      for u in exist:
        if u.email == body.email:
          conflict_error.append(
            ExceptionDetails(
              loc=['body', 'email'],
              msg='Email address already registered',
              type='type_error.email',
              input=body.email,
            )
          )
        if u.username == body.username:
          conflict_error.append(
            ExceptionDetails(
              loc=['body', 'username'],
              msg='Username already registered',
              type='type_error.username',
              input=body.username,
            )
          )
      raise RegistrationConflictException(detail=conflict_error)

    new_user = await repo.create(body=body)

    verify_token = email_verify_token_decoded(new_user.email)
    verify_url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/{api_tree['v1']['auth']['verify']['path']}/{verify_token}" # type: ignore
    send_verify_email_task.delay(
      to_email=new_user.email,
      context= {
        "username": new_user.username,
        'verify_url': verify_url
      },
    )


  return UserRegisterResponseSchema(
    message="Registration successful. Please check your email to verify your account. You have 24 hour to verify your account.",
  )



async def verify_service(
    verify_token: str,
    db: AsyncSession,
)-> UserVerifyResponseSchema:
  verify_email = email_verify_token_encoded(verify_token)

  async with ModelRepository[UserModel](db, UserModel) as repo:
    user = await repo.get_one(field= 'email',value= verify_email,)

    if user.is_verified:
      return UserVerifyResponseSchema(
        email=user.email,
        message='Email address already verified.',
      )

    user.set_verified()

  return UserVerifyResponseSchema(
    email=user.email,
    message='Email address verified successfully.'
  )

async def login_service(
    db: AsyncSession,
    redis_conn: Redis,
    body: UserLoginSchema,
    res: Response
):
  to_raise = InvalidCredentialsException(
    detail=[
      ExceptionDetails(
        loc=['body', 'password'],
        msg='',
        type='',
        input=body.password,
      ),
      ExceptionDetails(
        loc=['body', 'email'],
        msg='',
        type='',
        input=body.email,
      )
    ]
  )
  async with ModelRepository[UserModel](db, UserModel) as repo:
    try:
      user = await repo.get_one(field= 'email',value= body.email)
    except NotFoundException:
      raise to_raise
    if not password_verify(user.encoded_password, body.password):
      await repo.update(user.uid, {'failed_login_attempts': user.failed_login_attempts + 1})
      await db.commit()
      raise to_raise


    if not user.is_verified:
      raise EmailNotVerifiedException(
        detail=[ExceptionDetails(
          loc=['body', 'email'],
          msg='Your account has not been verified. Please check your email for the verification link.',
          type='type_error.account_not_verified',
          input=body.email,
        )]
      )
    if not user.is_active:
      raise InActiveUserException(
        detail=[ExceptionDetails(
          loc=['body', 'email'],
          msg='This account is currently inactive. Please contact support for assistance.',
          type='type_error.account_inactive',
          input=body.email,
        )]
      )

    session_uid = uuid7()
    refresh_jti = uuid7()
    access_token = create_access_token(user_id=user.uid, session_id=session_uid, jti=uuid7())
    refresh_token = create_refresh_token(user_id=user.uid, session_id=session_uid, jti=refresh_jti)

    await redis_conn.set(f'refresh:{session_uid}', str(refresh_jti), ex=(3600 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE))

  res.set_cookie(
    key=settings.REFRESH_TOKEN_COOKIE_NAME,
    value=refresh_token,
    httponly=True,
    secure= not settings.DEVELOP_MODE,
    samesite='lax' if settings.DEVELOP_MODE else 'none',
    path="/",
  )

  return UserLoginResponseSchema(
    email=user.email,
    message=f"Login successful. Welcome back, {user.username}!",
    token={
      'access_token': access_token,
    }
  )



async def refresh_service(
    db: AsyncSession,
    res: Response,
    redis_conn: Redis,
    refresh_token: str,
    access_token: str | None = None,
) -> UserRefreshTokenResponseSchema:
  try:
    refresh_claims = jwt_decode(refresh_token, is_verify=True)
  except ExpiredTokenException:
    res.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME,)
    raise

  if refresh_claims.type != 'refresh':
    raise InvalidTokenException(
      detail=[ExceptionDetails(
        loc=["cookie", "refresh_token"],
        type="value_error",
        input=None,
        msg="Can't use access token as refresh token."
      )],
      delete_cookies=[settings.REFRESH_TOKEN_COOKIE_NAME]
    )

  if access_token:
    access_claims = jwt_decode(access_token, is_verify=False)

    if access_claims is not None:
      if access_claims.type != 'access':
        raise InvalidTokenException(
          detail=[ExceptionDetails(
            loc=["cookie", "access_token"],
            type="value_error.invalid_type",
            input=None,
            msg="Can't use refresh token as access token."
          )]
        )


      if refresh_claims.session_id != access_claims.session_id:
        raise InvalidTokenSessionIdException(
          detail=[ExceptionDetails(
            loc=["cookie", "session_id"],
            type="value_error",
            input=None,
            msg="The session id of the refresh token don't match the access token."
          )]
        )


  if await redis_conn.exists(f'blacklist:{refresh_claims.jti}'):
    raise RefreshTokenBlacklistedException(
      detail=[ExceptionDetails(
        loc=["cookie", "blacklist"],
        type="value_error",
        input=None,
        msg="The refresh token has been blacklisted. Please login again or contact support for assistance."
      )],
      delete_cookies=[settings.REFRESH_TOKEN_COOKIE_NAME]
    )

  stored_jti = await redis_conn.get(f'refresh:{refresh_claims.session_id}')
  if not stored_jti:
    raise ExpiredTokenException(
      detail=[ExceptionDetails(
        loc=["cookie", "refresh_token"],
        type="value_error.session_expired",
        input=None,
        msg="Your session has expired. Please log in again."
      )],
      delete_cookies=[settings.REFRESH_TOKEN_COOKIE_NAME]
    )

  if stored_jti != refresh_claims.jti:
    await redis_conn.delete(f'refresh:{refresh_claims.session_id}')
    await redis_conn.set(f'blacklist:{refresh_claims.jti}', '1', ex=(3600 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE))

    raise TokenReusedException(
      detail=[ExceptionDetails(
        loc=["cookie", "refresh_token"],
        type="value_error.token_reuse_detected",
        input=None,
        msg="This session has been terminated for security reasons. Please log in again."
      )],
      delete_cookies=[settings.REFRESH_TOKEN_COOKIE_NAME]
    )

  refresh_jti = uuid7()
  access_token = create_access_token(user_id=UUID(refresh_claims.sub), session_id=UUID(refresh_claims.session_id), jti=uuid7())
  refresh_token = create_refresh_token(user_id=UUID(refresh_claims.sub), session_id=UUID(refresh_claims.session_id), jti=refresh_jti)
  await redis_conn.set(f'refresh:{refresh_claims.session_id}', str(refresh_jti), ex=(3600 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE))
  await redis_conn.set(f'blacklist:{refresh_claims.jti}', '1', ex=(3600 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE))

  res.set_cookie(
    key=settings.REFRESH_TOKEN_COOKIE_NAME,
    value=refresh_token,
    httponly=True,
    secure= not settings.DEVELOP_MODE,
    samesite='lax' if settings.DEVELOP_MODE else 'none',
    path="/",
  )

  async with ModelRepository[UserModel](db, UserModel) as repo:
    await repo.update(UUID(refresh_claims.sub), {'last_login_at': PROJECT_DATETIME.get_datetime()})

  return UserRefreshTokenResponseSchema(
    access_token=access_token,
  )


async def logout_service(
    refresh_token: str,
    redis_conn: Redis,
    res: Response,
):
  refresh_claims = jwt_decode(refresh_token, is_verify=False)

  await redis_conn.delete(f'refresh:{refresh_claims.session_id}')
  await redis_conn.set(f'blacklist:{refresh_claims.jti}', '1', ex=(3600 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE))

  res.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)

  return None


async def forgot_password_service(
    db: AsyncSession,
    body: UserForgotPasswordSchema,
    redis_conn: Redis
)-> UserForgotPasswordResponseSchema:

  reset_id = secrets.token_hex(32)

  res = {
    'reset_id': reset_id,
    'email': body.email,
    'message': 'The verification has been send successfully, please check your email.'
  }

  async with ModelRepository[UserModel](db, UserModel) as repo:
    try:
      user = await repo.get_one('email', value=body.email)
    except NotFoundException:
      return UserForgotPasswordResponseSchema(**res)

  if not user.is_verified:
    raise EmailNotVerifiedException(
      detail=[ExceptionDetails(
        loc=['body', 'email'],
        msg='Your account has not been verified. Please check your email for the verification link.',
        type='type_error.account_not_verified',
        input=body.email,
      )]
    )
  if not user.is_active:
    raise InActiveUserException(
      detail=[ExceptionDetails(
        loc=['body', 'email'],
        msg='This account is currently inactive. Please contact support for assistance.',
        type='type_error.account_inactive',
        input=body.email,
      )]
    )

  otp = f"{secrets.randbelow(1_000_000):06d}"

  send_password_reset_email_task.delay(
    to_email=user.email,
    context= {
      "otp": otp,
    },
  )

  otp_hash = otp_decoded(otp)
  now = PROJECT_DATETIME.get_datetime()

  data = OtpData(
    user_uid = str(user.uid),
    otp_hash = otp_hash,
    created_at = int(now.timestamp()),
    expires_at = int((now + timedelta(minutes=10)).timestamp()),
    attempt_count = 0
  )

  await redis_conn.set(f'reset:{reset_id}', data.model_dump_json(), ex=600)


  return UserForgotPasswordResponseSchema(**res)

async def reset_password_verify_service(
    body: UserResetPasswordVerifySchema,
    redis_conn: Redis
)-> UserResetPasswordVerifyResponseSchema:
  raw =  await redis_conn.get(f'reset:{body.reset_id}')
  logger.info(f'raw:{raw}')
  if not raw:
    raise InvalidResetIdException(
      detail=[ExceptionDetails(
        loc=['body', f'reset_id'],
        type='value_error',
        input=body.reset_id,
        msg="The reset id is invalid, please check the reset id."
      )]
    )

  data = json.loads(raw)
  data['attempt_count'] = data['attempt_count'] + 1

  if not otp_verify(data['otp_hash'],otp_decoded(body.opt)):
    ttl = await redis_conn.ttl(f"reset:{body.reset_id}")
    await redis_conn.set(f'reset:{body.reset_id}', json.dumps(data), ex= ttl if ttl > 0 else None)
    raise InvalidOtpException(
      detail=[ExceptionDetails(
        loc=['body', f'otp'],
        type='value_error',
        input=body.opt,
        msg="The otp hash is invalid, please check the otp hash."
      )]
    )

  await redis_conn.delete(f'reset:{body.reset_id}')
  verification_token = secrets.token_urlsafe(32)
  await redis_conn.set(f'password-reset-token:{verification_token}', value=data['user_uid'], ex=600)

  return UserResetPasswordVerifyResponseSchema(
    verification_token=verification_token
  )



async def change_password_service(
    body: UserChangePasswordSchema,
    redis_conn: Redis,
    db: AsyncSession
):
  user_uid =  await redis_conn.get(f'password-reset-token:{body.verification_token}')

  if not user_uid:
    raise ExpiredPasswordResetTokenException(
      detail=[ExceptionDetails(
        loc=['body', f'verification_token'],
        type='value_error',
        input=body.verification_token,
        msg="The verification token is invalid, please check the verification token."
      )]
    )

  async with ModelRepository[UserModel](db, UserModel) as repo:
    try:
      user = await repo.get_one('uid', user_uid)

      if password_verify(user.encoded_password, body.encoded_password):
        raise SamePasswordException(
          detail=[ExceptionDetails(
            loc=['body', 'password'],
            type='value_error',
            input=body.encoded_password,
            msg="The new password must be different from your current password."
          )]
        )
      user.set_password_reset(password_hash(body.encoded_password))
      await repo.update(obj_instance=user)
    except NotFoundException:
      raise InvalidPasswordResetTokenException(
        detail=[ExceptionDetails(
          loc=["body", "verification_token"],
          type="value_error",
          input=body.verification_token,
          msg="The verification token is invalid or has expired.",
        )]
      )

  await redis_conn.delete(f'password-reset-token:{body.verification_token}')
  return UserChangePasswordResponseSchema(
    message='Your password has been changed successfully.'
  )







