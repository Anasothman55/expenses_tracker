
from pydantic import ConfigDict, BaseModel

from app.infrastructure.db.models.currencies import  CurrenciesName, CurrenciesCode, CurrenciesSymbol


class CurrenciesCreateSchema(BaseModel):
  name: CurrenciesName
  code: CurrenciesCode
  symbol: CurrenciesSymbol

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )

