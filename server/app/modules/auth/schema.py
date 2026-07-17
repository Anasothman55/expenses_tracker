from typing import Annotated

from pydantic import BaseModel, Field, EmailStr, ConfigDict, StringConstraints, field_validator, AfterValidator

from app.core.security.password_hashing import password_hash
from app.infrastructure.db.models.users import UserUsername, UserEmail

UserPassword = Annotated[
  str,
  StringConstraints(max_length=128, min_length=8, strip_whitespace=True, ),
  Field(...,examples=['StrongPassword123']),
]

class UserRegisterSchema(BaseModel):
  username: UserUsername
  email: UserEmail
  encoded_password: UserPassword = Field(alias='password')

  @field_validator("encoded_password", mode="after")
  @classmethod
  def encode_password_validator(cls, value: str ):
    return password_hash(value)

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid',
  )

class UserLoginSchema(BaseModel):
  email: UserEmail
  password: UserPassword

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid',
  )


class UserForgotPasswordSchema(BaseModel):
  email: UserEmail

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid',
  )

class UserResetPasswordVerifySchema(BaseModel):
  reset_id: str
  opt: str = Field(..., max_length=6, min_length=6)

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid',
  )

class UserChangePasswordSchema(BaseModel):
  verification_token: str
  encoded_password: UserPassword = Field(alias='new_password')

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid',
  )


# Responses

class UserRegisterResponseSchema(BaseModel):
  message: str
  email_verified: bool = False


class UserVerifyResponseSchema(BaseModel):
  email: EmailStr
  message: str

class UserLoginResponseSchema(BaseModel):
  email: EmailStr
  message: str
  token: dict

class UserRefreshTokenResponseSchema(BaseModel):
  access_token: str

class UserForgotPasswordResponseSchema(BaseModel):
  email: EmailStr
  message: str
  reset_id: str

class UserResetPasswordVerifyResponseSchema(BaseModel):
  verification_token: str

class UserChangePasswordResponseSchema(BaseModel):
  message: str