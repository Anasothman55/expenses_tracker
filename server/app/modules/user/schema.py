from uuid import UUID
from pydantic import BaseModel

from app.infrastructure.db.models.users import UserModelValidation



class UserCurrencySchema(BaseModel):
  user_currencies: UUID



# response

class UserMeResponseSchema(UserModelValidation):
  pass

class UserCurrencyResponseSchema(UserModelValidation):
  pass

