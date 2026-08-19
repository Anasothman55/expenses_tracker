from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastcrud import FastCRUD, EndpointCreator
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


from .schema import UserCreateSchema, UserMeResponseSchema, UserUpdateSchema
from src.core.deps.db import get_db
from src.infrastructure.db.models import UserModel
from src.modules.auth.deps import get_current_user
from .service import currency_service, me_service





user_route = APIRouter(
  tags=["User"],
  dependencies=[Depends(get_current_user)],
)


@user_route.get('/me', response_model=UserMeResponseSchema, response_model_exclude={"encoded_password"}, status_code=200)
async def me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
  return await me_service(db,current_user.uid)

@user_route.post('/currency', response_model=UserMeResponseSchema, response_model_exclude={"encoded_password"}, status_code=status.HTTP_201_CREATED)
async def currency(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    body: UserUpdateSchema
):
  return await currency_service(db , body, current_user.uid)





















