from uuid import UUID
from decimal import Decimal
from datetime import date

from pydantic import EmailStr, Field, StringConstraints, BaseModel, StrictBool, ConfigDict
from datetime import datetime
from typing import Optional, Annotated

from sqlalchemy import Text, String, UUID as SqlUUID, ForeignKey, UniqueConstraint, Numeric, Enum as SqlEnum, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.shared.enums.tables import TransactionTypeEnum
from app.shared.utils.constant import PROJECT_DATETIME
from ..base import Base, EssentialColumns, EssentialColumnValidation


TransactionDescription = Annotated[str, StringConstraints(min_length=1, max_length=128, strip_whitespace=True), Field(..., examples=['but gas'])]
TransactionDecimal15_2 = Annotated[Decimal, Field(...,max_digits=15, decimal_places=2 ,examples=[57.99])]
TransactionDecimal6_5 = Annotated[Decimal, Field(...,max_digits=15, decimal_places=2 ,examples=[57.99])]

class TransactionsModelValidation(EssentialColumnValidation):

  description: TransactionDescription
  amount: TransactionDecimal15_2
  transaction_date: date
  transaction_type: TransactionTypeEnum
  note: str | None
  categories_uid: UUID | None
  account_currencies_uid: UUID
  exchange_rate: TransactionDecimal6_5
  account_currencies_amount: TransactionDecimal15_2

  account_currencies: UUID
  user_uid: UUID

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class TransactionsModel(EssentialColumns):
  __tablename__ = 'transactions'

  description: Mapped[str] = mapped_column(String(128), nullable=False,)
  amount: Mapped[Decimal] = mapped_column(Numeric(15,2), nullable=False)
  transaction_date: Mapped[date] = mapped_column(Date, nullable=False, default=PROJECT_DATETIME.get_date())
  transaction_type: Mapped[TransactionTypeEnum] = mapped_column(
    SqlEnum(TransactionTypeEnum, name="transaction_type_enum", create_type=True),
    nullable=False, default=TransactionTypeEnum.Expenses
  )
  note: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

  categories_uid: Mapped[UUID | None] = mapped_column(SqlUUID, ForeignKey('categories.uid', ondelete='RESTRICT'), default=None, nullable=True)

  account_currencies_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('currencies.uid', ondelete='RESTRICT') ,nullable=True, default=None)

  exchange_rate: Mapped[Decimal | None] = mapped_column(Numeric(6,5), nullable=True)
  account_currencies_amount: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)

  account_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('accounts.uid', ondelete='RESTRICT'), nullable=False)

  user_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)

  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> TransactionsModelValidation:
    return TransactionsModelValidation.model_validate(self)














