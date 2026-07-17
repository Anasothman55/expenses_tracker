from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import CurrenciesModel, UserModel
from app.modules.user.schema import UserCurrencySchema, UserCurrencyResponseSchema
from app.shared.utils.ctype import ExceptionDetails
from app.shared.utils.model_repository import ModelRepository


async def currency_service(
    db: AsyncSession,
    body: UserCurrencySchema,
    user_uid: UUID
)-> UserModel:
  async with ModelRepository[CurrenciesModel](db, CurrenciesModel) as repo:
    currency = await repo.get_one('uid', value=body.user_currencies)

  async with ModelRepository[UserModel](db, UserModel) as repo:
    user = await repo.get_one('uid', user_uid)

    if user.user_currencies is not None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=[ExceptionDetails(
          loc=['body', 'user_currencies'],
          input={'user_currencies': user.user_currencies},
          type='already_exists.error',
          msg='User currencies already exists.'
        )]
      )

    return await repo.update(user_uid, body, None)





