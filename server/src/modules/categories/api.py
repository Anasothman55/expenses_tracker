from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query
from fastcrud import FastCRUD, EndpointCreator
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import UserModel
from src.infrastructure.db.models.categories import CategoriesModel, CategoriesModelValidation
from src.core.deps.db import get_db
from src.modules.auth.deps import get_current_user
from .service import delete_service, create_service, update_service, get_all_service, get_one_service, categories_crud
from .schema import CategoriesCreateSchema, CategoriesUpdateSchema, CategoriesResponseSchema



# ---- 1. Rename generated endpoints ----

endpoint_categories = EndpointCreator(
  session=get_db,
  model=CategoriesModel,
  crud=categories_crud,
  create_schema=None,
  update_schema=CategoriesUpdateSchema,
  deleted_at_column='deleted_at',
  select_schema=CategoriesResponseSchema,
  tags=["Categories"],
)

# ---- 2. Only expose the methods you actually want ----
endpoint_categories.add_routes_to_router(
  included_methods=[
    "read",
    "read_multi",
    "update",
    "delete",
    "db_delete",
  ],
  read_deps=[get_current_user],
  read_multi_deps=[get_current_user],
  update_deps=[get_current_user],
  delete_deps=[get_current_user],
  db_delete_deps=[get_current_user],
)


@endpoint_categories.router.post('/', tags=["Categories"], response_model=CategoriesResponseSchema ,status_code=status.HTTP_201_CREATED)
async def create(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: CategoriesCreateSchema,
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> CategoriesResponseSchema:
  return await create_service(body,db, current_user.uid)

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


