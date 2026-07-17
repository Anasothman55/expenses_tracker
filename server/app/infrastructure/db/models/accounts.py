from uuid import UUID

from pydantic import EmailStr, Field, StringConstraints, BaseModel, StrictBool, ConfigDict
from datetime import datetime
from typing import Optional, Annotated

from sqlalchemy import Text, String, Boolean, Date, DateTime, Integer, Index, text, UUID as SqlUUID, ForeignKey, \
  Enum as SqlEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.shared.enums.tables import AccountTypeEnum
from app.shared.utils.constant import PROJECT_DATETIME
from ..base import Base, EssentialColumns, EssentialColumnValidation


AccountTitle = Annotated[str, StringConstraints(max_length=64, min_length=2, strip_whitespace=True), Field(..., examples=['My Wallet'])]


class AccountsModelValidation(EssentialColumnValidation):
  title: AccountTitle
  account_type: AccountTypeEnum

  account_currencies: UUID

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class AccountsModel(EssentialColumns):
  __tablename__ = 'accounts'

  title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
  account_type: Mapped[AccountTypeEnum] = mapped_column(
    SqlEnum(AccountTypeEnum, name="account_type_enum", create_type=True),
    nullable=False, default=AccountTypeEnum.Wallet
  )

  user_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
  account_currencies: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('currencies.uid', ondelete='RESTRICT') ,nullable=True, default=None)

  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> AccountsModelValidation:
    return AccountsModelValidation.model_validate(self)

  __table_args__ = (
    UniqueConstraint('user_uid','title', 'account_type', name='type_title_user_uid'),
  )












