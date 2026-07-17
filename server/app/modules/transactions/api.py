from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.deps import get_current_user
from app.core.deps.db import get_db
from .service import delete_service, create_service, update_service, get_all_service, get_one_service


transactions_route = APIRouter(
  tags=["Transactions"],
  dependencies=[Depends(get_current_user)]
)



@transactions_route.get('/')
async def get_all(
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await get_all_service(db)

@transactions_route.post('/')
async def create(
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await create_service('', db)

@transactions_route.get('/{uid}/')
async def get_one(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await get_one_service( uid, db)

@transactions_route.put('/{uid}/')
async def update(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await update_service( uid, db)

@transactions_route.delete('/{uid}/')
async def delete(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await delete_service( uid, db)





