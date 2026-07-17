from uuid import UUID

from pydantic import EmailStr, Field, StringConstraints, BaseModel, StrictBool, ConfigDict
from datetime import datetime
from typing import Optional, Annotated

from sqlalchemy import Text, String, Boolean, Date, DateTime, Integer, Index, text, UUID as SqlUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.shared.utils.constant import PROJECT_DATETIME
from ..base import Base, EssentialColumns, EssentialColumnValidation

UserUsername = Annotated[
  str,
  StringConstraints(
    min_length=3,
    max_length=128,
    strip_whitespace=True,
  ),
  Field(examples=["AnasAS"]),
]


UserEmail = Annotated[
  EmailStr, Field(...,max_length=128, examples=['anasothman@gmail.com'])
]



UserIsActive = Annotated[
  StrictBool,
  Field(default=False),
]

UserIsVerified = Annotated[
  StrictBool,
  Field(default=False),
]

UserFailedLoginAttempts = Annotated[
  int,
  Field(default=0, ge=0),
]


class UserModelValidation(EssentialColumnValidation):
  email: UserEmail
  username: UserUsername
  encoded_password: str = Field(exclude=True)

  is_active: UserIsActive
  is_verified: UserIsVerified

  failed_login_attempts: UserFailedLoginAttempts = 0
  last_login_at: datetime | None = None
  password_changed_at: datetime | None = None

  user_currencies: UUID | None = None

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class UserModel(EssentialColumns):
  __tablename__ = 'users'

  email: Mapped[EmailStr] = mapped_column(String(128), index=True, nullable=False)
  username: Mapped[str] = mapped_column(String(128), nullable=False)
  encoded_password: Mapped[str] = mapped_column(String(256), nullable=False)

  is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
  is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

  failed_login_attempts: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
  last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=settings.TIME_ZONE), nullable=True)
  password_changed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=settings.TIME_ZONE), nullable=True)

  user_currencies: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('currencies.uid', ondelete='RESTRICT') ,nullable=True, default=None)

  def set_soft_delete(self):
    super().set_soft_delete()
    self.is_active = False

  def set_verified(self):
    # we should call this function once
    self.is_verified = True
    self.is_active = True

  def set_password_reset(self, new_password: str):
    self.encoded_password = new_password
    self.password_changed_at = PROJECT_DATETIME.get_datetime()

  def set_failed_login_attempts(self):
    self.failed_login_attempts = self.failed_login_attempts + 1

  def validate(self) -> UserModelValidation:
    return UserModelValidation.model_validate(self)

  __table_args__ = (
    Index(
      'uq_users_email_active',
      'email',
      unique=True,
      postgresql_where=text('deleted_at IS NULL'),
    ),
    Index(
      'uq_users_username_active',
      'username',
      unique=True,
      postgresql_where=text('deleted_at IS NULL'),
    ),
  )












