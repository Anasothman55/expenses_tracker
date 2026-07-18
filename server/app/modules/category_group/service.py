from typing import Sequence, Any, List
from uuid import UUID

from fastapi_pagination import Params
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.infrastructure.db.models import CategoryGroupModel
from app.shared.utils.model_repository import ModelRepository
from app.shared.utils.sql_operator import OPERATORS
from .schema import CategoryGroupCreateSchema, CategoryGroupFilterAll

  
async def get_all_service(
    db: AsyncSession,
    params: Params,
    filters: List[CategoryGroupFilterAll],
    user_uid: UUID ,
    is_pagination: bool = False,
    include_deleted: bool = False,
)-> Sequence[CategoryGroupModel] | Any:

  stmt: Select[tuple[CategoryGroupModel]] = (select(CategoryGroupModel).where(CategoryGroupModel.user_uid == user_uid))

  for f in filters:
    attr = getattr(CategoryGroupModel, f.column.value)
    op_func = OPERATORS[f.operator.value]
    stmt = stmt.where(op_func(attr, f.value))



  async with ModelRepository[CategoryGroupModel](db, CategoryGroupModel) as repo:
    return await repo.get_all(
      is_pagination=is_pagination,
      include_deleted=include_deleted,
      select_stmt=stmt,
      params=params
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
    db: AsyncSession
):
  pass

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



