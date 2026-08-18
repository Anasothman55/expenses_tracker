from decimal import Decimal
from uuid import UUID

from pydantic import EmailStr, Field, StringConstraints, BaseModel, StrictBool, ConfigDict
from datetime import datetime, date
from typing import Optional, Annotated

from sqlalchemy import Text, String, Boolean, Date, DateTime, Integer, Index, text, UUID as SqlUUID, ForeignKey, \
  Enum as SqlEnum, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.core.config import settings
from src.shared.enums.tables import AccountTypeEnum, AccouontLoanTypeEnum
from src.shared.utils.constant import PROJECT_DATETIME
from ..base import Base, EssentialColumns, EssentialColumnValidation


AccountTitle = Annotated[str, StringConstraints(max_length=64, min_length=2, strip_whitespace=True), Field(..., examples=['My Wallet'])]


class AccountsModelValidation(EssentialColumnValidation):
  title: AccountTitle
  balance: Decimal
  balance_start: date
  loan_start: date | None = None
  loan_end: date | None = None
  loan_finish: date | None = None
  loan_type: AccouontLoanTypeEnum
  account_type: AccountTypeEnum | None = None

  account_currencies: UUID

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class AccountsModel(EssentialColumns):
  __tablename__ = 'accounts'
  
  title: Mapped[str] = mapped_column(String(64), nullable=False)
  balance: Mapped[Decimal] = mapped_column(Numeric, nullable=False, )
  balance_start: Mapped[date] = mapped_column(Date, default=PROJECT_DATETIME.get_date)
  loan_start: Mapped[date | None] = mapped_column(Date)
  loan_end: Mapped[date | None] = mapped_column(Date)
  loan_finish: Mapped[date | None] = mapped_column(Date)
  
  #enum
  account_type: Mapped[AccountTypeEnum] = mapped_column(
    SqlEnum(AccountTypeEnum, name="account_type_enum", create_type=True),
    nullable=False, default=AccountTypeEnum.Wallet
  )
  loan_type: Mapped[AccouontLoanTypeEnum | None] = mapped_column(
    SqlEnum(AccouontLoanTypeEnum, name="account_loan_type_enum", create_type=True),
    nullable=False,
  )

  # prelations
  user_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
  account_currencies: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('currencies.uid', ondelete='RESTRICT') ,nullable=True, default=None)

  # functionality
  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> AccountsModelValidation:
    return AccountsModelValidation.model_validate(self)

  __table_args__ = (
    UniqueConstraint('user_uid','title', 'account_type', name='type_title_user_uid'),
  )












