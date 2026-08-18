from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.modules.currencies.schema import CurrenciesUserResponseSchema
from src.infrastructure.db.models.users import UserModelValidation


class UserCreateSchema(BaseModel):
  pass

  model_config = ConfigDict(
    extra="forbid"
  )

class UserUpdateSchema(BaseModel):
  user_currencies: UUID

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid"
  )



# response

class UserMeResponseSchema(UserModelValidation):
  currency: CurrenciesUserResponseSchema
