from typing import Literal

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error

from app.core.config import settings

ph = PasswordHasher()

def password_hash(password: str) -> str:
  return ph.hash(
    settings.PASSWORD_SECRET.get_secret_value()+password
  )

def password_verify(encoded_password: str, password: str) -> Literal[True,False]:
  try:
    return ph.verify(
      encoded_password,
      settings.PASSWORD_SECRET.get_secret_value()+password
    )
  except Argon2Error:
    return False





