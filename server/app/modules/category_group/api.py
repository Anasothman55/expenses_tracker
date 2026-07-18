from uuid import UUID
from typing import Annotated, List

from fastapi.params import Body
from rich import print

from fastapi import APIRouter, Depends, status, Path, Query
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps.db import get_db
from app.infrastructure.db.models import UserModel
from app.modules.auth.deps import get_current_user
from .service import delete_service, create_service, update_service, get_all_service, get_one_service
from .schema import CategoryGroupResponseAllSchema, CategoryGroupQueryAll, CategoryGroupFilterAll, \
  CategoryGroupCreateSchema
from .deps import parse_category_group_filters

category_group_route = APIRouter(
  tags=["Category Group"],
  dependencies=[Depends(get_current_user)]
)



@category_group_route.get('/', response_model=Page[CategoryGroupResponseAllSchema] | List[CategoryGroupResponseAllSchema])
async def get_all(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    params: Annotated[Params, Depends()],
    query: Annotated[CategoryGroupQueryAll, Depends()],
    filters: Annotated[List[CategoryGroupFilterAll], Depends(parse_category_group_filters)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await get_all_service(db,filters=filters,user_uid=current_user.uid ,params=params, **query.model_dump())

@category_group_route.post('/')
async def create(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    body: Annotated[CategoryGroupCreateSchema, Body() ]
):
  return await create_service(body, db, user_uid=current_user.uid )

@category_group_route.get('/{uid}/')
async def get_one(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await get_one_service( uid, db)

@category_group_route.put('/{uid}/')
async def update(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await update_service( uid, db)

@category_group_route.delete('/{uid}/')
async def delete(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await delete_service( uid, db)




