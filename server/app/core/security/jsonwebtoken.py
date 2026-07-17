from typing import  Literal
from datetime import timedelta
from uuid import UUID, uuid7

from fastapi.security import HTTPBearer
from joserfc import jwt
from joserfc.jwt import JWTClaimsRegistry
from joserfc.jwk import OctKey
from joserfc.errors import (
  ExpiredTokenError,
  BadSignatureError,
  DecodeError,
  MissingClaimError,
  InvalidClaimError,
  UnsupportedAlgorithmError,
  JoseError,
)
from loguru import logger

from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions.auth import (
  JoseException,
  InvalidTokenException,
  TokenSignatureException,
  MissingTokenClaimException,
  InvalidTokenClaimException,
  UnsupportedTokenAlgorithmException,
  ExpiredTokenException,
)
from app.shared.utils.constant import PROJECT_DATETIME
from app.shared.utils.ctype import ExceptionDetails


bearer = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
  sub: str
  session_id: str
  jti: str
  type: Literal["access", "refresh"]
  ait: int
  exp: int

KEY = OctKey.import_key(settings.JWT_SECRET_KEY.get_secret_value())
ALGORITHMS = [settings.JWT_ALGORITHM]

def jwt_encoded(data: TokenPayload) -> str:
  return jwt.encode(
    header={"alg": settings.JWT_ALGORITHM},
    key=KEY,
    claims=data.model_dump().copy(),
    algorithms=ALGORITHMS
  )


def jwt_decode(token: str, is_verify: bool = True) -> TokenPayload:
  decoded_claims: dict | None = None
  try:
    token_obj = jwt.decode(token, key=KEY, algorithms=ALGORITHMS)
    decoded_claims = token_obj.claims
    if is_verify:
      claim_registry = JWTClaimsRegistry(exp = {"essential": True})
      claim_registry.validate(decoded_claims)

    return TokenPayload(**decoded_claims)
  except ExpiredTokenError as exc:
    logger.debug(exc)
    raise ExpiredTokenException() from exc
  except BadSignatureError as exc:
    raise TokenSignatureException() from exc

  except MissingClaimError as exc:
    raise MissingTokenClaimException(
      detail=[ExceptionDetails(
        loc=["token", "claim_name"],
        msg= f"Missing claim: {exc.claim}",
        type='type_error.missing_claim',
        input=decoded_claims
      )]
    ) from exc
  except InvalidClaimError as exc:
    raise InvalidTokenClaimException() from exc
  except UnsupportedAlgorithmError as exc:
    raise UnsupportedTokenAlgorithmException() from exc
  except DecodeError as exc:
    raise InvalidTokenException() from exc
  except JoseError as exc:
    raise JoseException(
      detail=[ExceptionDetails(
        loc=["token"],
        msg= f"Invalid token: {exc}",
        type='type_error.invalid_token',
        input=token
      ), exc.__dict__]
    ) from exc


def create_access_token(
    user_id: UUID,
    session_id: UUID,
    jti: UUID
) -> str:

  now = PROJECT_DATETIME.get_datetime()

  payload = TokenPayload(
    sub= str(user_id),
    session_id= str(session_id),
    jti= str(jti),
    type= "access",
    ait= int(now.timestamp()),
    exp= int((now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTE)).timestamp()),
  )
  return jwt_encoded(payload)

def create_refresh_token(
    user_id: UUID,
    session_id: UUID,
    jti: UUID
):
  now = PROJECT_DATETIME.get_datetime()
  payload= TokenPayload(
    sub= str(user_id),
    session_id= str(session_id),
    jti= str(jti),
    type= "refresh",
    ait= int(now.timestamp()),
    exp= int((now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)).timestamp())
  )

  return jwt_encoded(payload)




