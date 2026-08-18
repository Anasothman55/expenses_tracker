from typing import TypedDict

from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadData, SignatureExpired
from pydantic import EmailStr

from src.core.config import settings
from src.core.errors.auth import EmailVerifyTokenException, EmailVerifyTokenExpiredException

serializer = URLSafeSerializer(settings.EMAIL_VERIFY_TOKEN_SECRET_KEY.get_secret_value())



def email_verify_token_decoded(email: EmailStr)-> str:
  return serializer.dumps(
    email,
    salt=settings.EMAIL_VERIFY_TOKEN_SECRET_SALT.get_secret_value()
  )

def email_verify_token_encoded(token: str, max_age: int = 3600 * 24)-> str:
  """ this function will return the user email """
  try:
    return serializer.loads(
      token,
      salt=settings.EMAIL_VERIFY_TOKEN_SECRET_SALT.get_secret_value(),
      max_age=max_age,
    )
  except SignatureExpired as es:
    raise EmailVerifyTokenExpiredException(detail=[str(es)])
  except BadData as eb:
    raise EmailVerifyTokenException(detail=[str(eb)])














