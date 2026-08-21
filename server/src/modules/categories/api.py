from uuid import UUID
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, status, Path, Query
from fastcrud import FastCRUD, EndpointCreator
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import UserModel
from src.infrastructure.db.models.categories import CategoriesModel, CategoriesModelValidation
from src.core.deps.db import get_db
from src.modules.auth.deps import get_current_user
from .service import hard_delete_service, create_service, update_service, get_all_service, get_one_service, categories_crud, delete_service
from .schema import CategoriesCreateSchema, CategoriesUpdateSchema, CategoriesResponseSchema, \
  CategoriesReadMultiResponse, CategoriesReadMultiFilter, CategoriesReadResponse

categories_route = APIRouter(
  tags=["Categories"],
  dependencies=[Depends(get_current_user)]
)

@categories_route.get('/', response_model=CategoriesReadMultiResponse)
async def get_multi(
    filters: Annotated[CategoriesReadMultiFilter, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
  return await get_all_service( db, current_user.uid, filters)


@categories_route.post('/', response_model=CategoriesResponseSchema ,status_code=status.HTTP_201_CREATED)
async def create(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: CategoriesCreateSchema,
    current_user: Annotated[UserModel, Depends(get_current_user)]
) :
  return await create_service(body,db, current_user.uid)

@categories_route.get('/{uid}', response_model=CategoriesReadResponse ,status_code=status.HTTP_201_CREATED)
async def get(
    uid: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)]
) :
  return await get_one_service(uid, db, current_user.uid)

@categories_route.put('/{uid}', response_model=CategoriesResponseSchema ,status_code=status.HTTP_201_CREATED)
async def put(
    uid: UUID,
    body: CategoriesUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)]
) :
  return await update_service(uid, db, current_user.uid, body)

# @categories_route.delete('/hard/{uid}' ,status_code=status.HTTP_204_NO_CONTENT)
# async def hard_delete(
#     uid: UUID,
#     db: Annotated[AsyncSession, Depends(get_db)],
#     current_user: Annotated[UserModel, Depends(get_current_user)]
# ) :
#   return await hard_delete_service( current_user.uid,uid, db)


@categories_route.delete('/{uid}' ,status_code=status.HTTP_202_ACCEPTED)
async def delete(
    uid: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    hard: Annotated[bool, Query()] | None = None
) :
  if hard:
    return await hard_delete_service( current_user.uid,uid, db)
  return await delete_service( current_user.uid,uid, db)


# categories_route = APIRouter(
#   tags=["Categories"],
#   dependencies=[Depends(get_current_user)]
# )
#
#
# @categories_route.get('/')
# async def get_all(
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await get_all_service(db)
#

#
#
# @categories_route.get('/{uid}/')
# async def get_one(
#     uid: Annotated[UUID, Path()],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await get_one_service( uid, db)
#
# @categories_route.put('/{uid}/')
# async def update(
#     uid: Annotated[UUID, Path()],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await update_service( uid, db)
#
# @categories_route.delete('/{uid}/')
# async def delete(
#     uid: Annotated[UUID, Path()],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await delete_service( uid, db)


