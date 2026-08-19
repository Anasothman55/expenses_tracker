
from uuid import UUID

from pydantic import ConfigDict, BaseModel

from src.infrastructure.db.models.currencies import  CurrenciesName, CurrenciesCode, CurrenciesSymbol


class CurrenciesResponseSchema(BaseModel):
  uid: UUID
  name: CurrenciesName
  code: CurrenciesCode
  symbol: CurrenciesSymbol

class CurrenciesUserResponseSchema(CurrenciesResponseSchema):
  name: CurrenciesName
  code: CurrenciesCode
  symbol: CurrenciesSymbol

class CurrenciesCreateSchema(BaseModel):
  name: CurrenciesName
  code: CurrenciesCode
  symbol: CurrenciesSymbol

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )

class CurrenciesUpdateSchema(BaseModel):
  name: CurrenciesName | None = None
  code: CurrenciesCode | None = None
  symbol: CurrenciesSymbol | None = None

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )