from typing import Sequence, Any, List
from uuid import UUID
from rich import print

from fastapi_pagination import Params
from fastcrud import FastCRUD, compute_offset, paginated_response
from fastcrud.types import GetMultiResponseModel, GetMultiResponseDict
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.utils.fastcrud_filter import FilterType
from src.modules.categories.schema import CategoriesResponseSchema
from src.infrastructure.db.models import CategoriesModel
from src.infrastructure.db.models import CategoryGroupModel
from src.shared.utils.model_repository import ModelRepository
from src.shared.utils.sql_operator import OPERATORS
from .schema import CategoryGroupCreateSchema, CategoryGroupFilterAll, CategoryGroupResponseSchema, \
  CategoryGroupReadMultiFilter, CategoryGroupResponseAllSchema

category_group_crud = FastCRUD(CategoryGroupModel)


async def get_all_service(
    db: AsyncSession,
    user_uid: UUID,
    filters: CategoryGroupReadMultiFilter,
):
  dumped_filter = filters.model_dump(exclude_none=True, by_alias=True)
  page = dumped_filter.pop("page", 1)
  items_per_page = dumped_filter.pop("items_per_page", 100)
  offset = dumped_filter.pop("offset", compute_offset(page=page, items_per_page=items_per_page))
  limit = dumped_filter.pop("limit", items_per_page)
  sort_columns = dumped_filter.pop("sort_columns", None)
  sort_orders = dumped_filter.pop("sort_orders", None)

  groups = await category_group_crud.get_multi(
    db=db,
    schema_to_select=CategoryGroupResponseAllSchema,
    return_as_model=True,
    offset=offset,
    limit=limit,
    sort_columns=sort_columns,
    sort_orders=sort_orders,
    user_uid=user_uid,
    **filters.preprocess(dumped_filter)
  )

  return paginated_response(
    page=page,
    items_per_page=items_per_page,
    crud_data=groups
  )


async def create_service(
    body: CategoryGroupCreateSchema,
    db: AsyncSession,
    user_uid: UUID ,
)-> CategoryGroupModel:
  async with ModelRepository[CategoryGroupModel](db, CategoryGroupModel) as repo:
    return await repo.create({**body.model_dump(), 'user_uid': user_uid })


async def get_one_service(
    uid: UUID,
    db: AsyncSession,
    user_uid: UUID,
) :
  group = await category_group_crud.get_joined(
    db=db,
    schema_to_select=CategoryGroupResponseSchema,
    join_model=CategoriesModel,
    join_prefix="categories",
    join_schema_to_select=CategoriesResponseSchema,   # only name, symbol, code
    join_type="left",
    nest_joins=True,
    relationship_type="one-to-many",
    **{"user_uid": user_uid, 'uid': uid},
  )

  return group

async def update_service(
    uid: UUID,
    db: AsyncSession
):
  pass

async def delete_service(
    uid: UUID,
    db: AsyncSession
):
  pass



