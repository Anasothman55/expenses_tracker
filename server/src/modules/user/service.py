from uuid import UUID
from rich import print

from fastapi import HTTPException, status
from fastcrud import FastCRUD
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only, raiseload

from src.infrastructure.db.models import CurrenciesModel, UserModel
from src.modules.user.schema import UserUpdateSchema, UserMeResponseSchema, CurrenciesUserResponseSchema
from src.shared.utils.ctype import ExceptionDetails
from src.shared.utils.model_repository import ModelRepository

user_crud = FastCRUD(UserModel)

async def me_service(db: AsyncSession, user_uid: UUID):

  user = await user_crud.get_joined(
    db=db,
    schema_to_select=UserMeResponseSchema,
    join_model=CurrenciesModel,
    join_prefix="currency",
    join_schema_to_select=CurrenciesUserResponseSchema,   # only name, symbol, code
    join_type="left",
    nest_joins=True,
    relationship_type="one-to-one",
    **{"uid": user_uid},
  )

  print(user)

  # async with ModelRepository[UserModel](db, UserModel) as repo:
  #   stmt = select(UserModel).options(
  #     joinedload(UserModel.currency).options(
  #       load_only(
  #         CurrenciesModel.name,
  #         CurrenciesModel.symbol,
  #         CurrenciesModel.code,
  #       )
  #     )
  #   )

  #   user = await repo.get_one('uid', user_uid, options=None, include_deleted=False, select_stmt=stmt)
  return user


async def currency_service(
    db: AsyncSession,
    body: UserUpdateSchema,
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

    data = await repo.update(user_uid, body, None)
    data.currency = currency
    return data





