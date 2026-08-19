from uuid import UUID

from typing import Annotated

from fastapi.params import Body
from fastcrud import EndpointCreator, FastCRUD, crud_router
from rich import print

from fastapi import APIRouter, Depends, dependencies, status, Path, Query
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps.db import get_db
from src.infrastructure.db.models import UserModel
from src.infrastructure.db.models.category_group import CategoryGroupModel,CategoryGroupModelValidation
from src.modules.auth.deps import get_current_user
from .service import delete_service, create_service, update_service, get_all_service, get_one_service, category_group_crud
from .schema import CategoryGroupResponseAllSchema, CategoryGroupQueryAll, CategoryGroupFilterAll, \
  CategoryGroupCreateSchema, CategoryGroupUpdateSchema, CategoryGroupResponseSchema
from .deps import parse_category_group_filters


# ---- 1. Rename generated endpoints ----

endpoint_category_group = EndpointCreator(
  session=get_db,
  model=CategoryGroupModel,
  crud=category_group_crud,
  create_schema=None,
  update_schema=CategoryGroupUpdateSchema,
  deleted_at_column='deleted_at',
  select_schema=CategoryGroupResponseAllSchema,

  tags=["Category Group"],
)

# ---- 2. Only expose the methods you actually want ----
endpoint_category_group.add_routes_to_router(
  included_methods=[
    "read_multi",
    "update",
    "delete",
    "db_delete",
  ],
  read_multi_deps=[get_current_user],
  update_deps=[get_current_user],
  delete_deps=[get_current_user],
  db_delete_deps=[get_current_user],

)

@endpoint_category_group.router.post("/", tags=['Category Group'], response_model=CategoryGroupResponseAllSchema)
async def create(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: CategoryGroupCreateSchema,
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
  return await create_service(body,db, current_user.uid)


@endpoint_category_group.router.get('/{uid}/', tags=['Category Group'], response_model=CategoryGroupResponseSchema)
async def get_one(
    uid: Annotated[UUID, Path()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
  return await get_one_service( uid, db, current_user.uid)



# category_group_route = APIRouter(
#   tags=["Category Group"],
#   dependencies=[Depends(get_current_user)]
# )



# @category_group_route.get('/', response_model=Page[CategoryGroupResponseAllSchema] | list[CategoryGroupResponseAllSchema])
# async def get_all(
#     current_user: Annotated[UserModel, Depends(get_current_user)],
#     params: Annotated[Params, Depends()],
#     query: Annotated[CategoryGroupQueryAll, Depends()],
#     filters: Annotated[list[CategoryGroupFilterAll], Depends(parse_category_group_filters)],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await get_all_service(db,filters=filters,user_uid=current_user.uid ,params=params, **query.model_dump())

# @category_group_route.post('/')
# async def create(
#     current_user: Annotated[UserModel, Depends(get_current_user)],
#     db: Annotated[AsyncSession, Depends(get_db)],
#     body: Annotated[CategoryGroupCreateSchema, Body() ]
# ):
#   return await create_service(body, db, user_uid=current_user.uid )



# @category_group_route.put('/{uid}/')
# async def update(
#     uid: Annotated[UUID, Path()],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await update_service( uid, db)

# @category_group_route.delete('/{uid}/')
# async def delete(
#     uid: Annotated[UUID, Path()],
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await delete_service( uid, db)




