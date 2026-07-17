from pydantic import  Field, StringConstraints, ConfigDict

from typing import Annotated

from sqlalchemy import  String, Index, text, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from ..base import EssentialColumns, EssentialColumnValidation



CurrenciesName = Annotated[str, Field(..., max_length=64, examples=['usa dollar'])]
CurrenciesCode = Annotated[str, StringConstraints(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$"), Field(..., examples=['USD'])]
CurrenciesSymbol = Annotated[str, Field(..., max_length=10, examples=['$'])]

class CurrenciesModelValidation(EssentialColumnValidation):

  name: CurrenciesName
  code: CurrenciesCode
  symbol: CurrenciesSymbol

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class CurrenciesModel(EssentialColumns):
  __tablename__ = 'currencies'

  name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
  code: Mapped[str] = mapped_column(CHAR(3), nullable=False, unique=True)
  symbol: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> CurrenciesModelValidation:
    return CurrenciesModelValidation.model_validate(self)


