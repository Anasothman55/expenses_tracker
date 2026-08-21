from uuid import UUID

from fastapi import HTTPException
from fastcrud import FastCRUD, compute_offset, paginated_response
from fastcrud.exceptions.http_exceptions import NotFoundException, CustomException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

# from src.core.errors.sql import NotFoundException
from src.shared.utils.constant import PROJECT_DATETIME
from src.shared.utils.model_repository import ModelRepository
from src.infrastructure.db.models.categories import CategoriesModel, CategoriesModelValidation
from .schema import CategoriesCreateSchema, CategoriesResponseSchema, CategoriesReadMultiFilter, CategoriesUpdateSchema

categories_crud = FastCRUD(CategoriesModel)



async def get_all_service(
    db: AsyncSession,
    user_uid: UUID,
    filters: CategoriesReadMultiFilter,
):
  dumped_filter = filters.model_dump(exclude_none=True, by_alias=True)
  page = dumped_filter.pop("page", 1)
  items_per_page = dumped_filter.pop("items_per_page", 100)
  offset = dumped_filter.pop("offset", compute_offset(page=page, items_per_page=items_per_page))
  limit = dumped_filter.pop("limit", items_per_page)
  sort_columns = dumped_filter.pop("sort_columns", None)
  sort_orders = dumped_filter.pop("sort_orders", None)
  include_deleted = dumped_filter.pop("include_deleted", False)

  category = await categories_crud.get_multi(
    db=db,
    schema_to_select=CategoriesResponseSchema,
    return_as_model=True,
    offset=offset,
    limit=limit,
    sort_columns=sort_columns,
    sort_orders=sort_orders,
    user_uid=user_uid,
    **({'deleted_at__is': None} if not include_deleted else {}),
    **filters.preprocess(dumped_filter)
  )

  return paginated_response(
    page=page,
    items_per_page=items_per_page,
    crud_data=category
  )


async def create_service(
    body: CategoriesCreateSchema,
    db: AsyncSession,
    user_uid: UUID,
)-> CategoriesModel:
  async with ModelRepository[CategoriesModel](db, CategoriesModel) as repo:
    return await repo.create({**body.model_dump(), 'user_uid': user_uid })


async def get_one_service(
    uid: UUID,
    db: AsyncSession,
    user_uid: UUID,
):
  pass

async def update_service(
    uid: UUID,
    db: AsyncSession,
    user_uid: UUID,
    body: CategoriesUpdateSchema
):
  async with ModelRepository[CategoriesModel](db, CategoriesModel) as repo:
    old = await repo.get_one(include_deleted=False,condition=(
      and_(
        CategoriesModel.user_uid == user_uid,
        CategoriesModel.uid == uid,
      ),
    ))

    for k,v in body.model_dump(exclude_none=True, exclude_unset=True).items():
      setattr(old, k, v)

    return await repo.update(obj_instance=old)


async def hard_delete_service(
    user_uid: UUID,
    uid: UUID,
    db: AsyncSession
):
  await categories_crud.db_delete(db=db, uid=uid, user_uid=user_uid)

async def delete_service(
    user_uid: UUID,
    uid: UUID,
    db: AsyncSession
):
  async with ModelRepository[CategoriesModel](db, CategoriesModel) as repo:
    await repo.get_one('uid', uid)
  await categories_crud.update(
    db=db,
    object={
      "deleted_at": PROJECT_DATETIME.get_datetime(),
    },
    uid=uid,
    user_uid=user_uid
  )

  return {
    "message": "Item soft deleted successfully",
  }


