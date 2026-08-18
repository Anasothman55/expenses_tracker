from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps.db import get_db
from src.infrastructure.db.models import UserModel
from src.modules.auth.deps import get_current_user
from src.modules.user.schema import UserMeResponseSchema, UserCurrencySchema, UserCurrencyResponseSchema
from .service import currency_service

user_route = APIRouter(
  tags=["User"],
  dependencies=[Depends(get_current_user)],
)


@user_route.get('/me', response_model=UserMeResponseSchema, response_model_exclude={"encoded_password"}, status_code=200)
async def me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
  return current_user.validate()

@user_route.post('/currency', response_model=UserCurrencyResponseSchema, response_model_exclude={"encoded_password"}, status_code=status.HTTP_202_ACCEPTED)
async def currency(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    body: UserCurrencySchema
):
  return await currency_service(db , body, current_user.uid)





















