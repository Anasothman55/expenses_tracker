from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.utils.model_repository import ModelRepository
from src.infrastructure.db.models.categories import CategoriesModel, CategoriesModelValidation
from .schema import CategoriesCreateSchema, CategoriesResponseSchema

categories_crud = FastCRUD(CategoriesModel)

class CategoriesCreateInternalSchema(CategoriesCreateSchema):
  uid: UUID

async def create_service(
    body: CategoriesCreateSchema,
    db: AsyncSession,
    user_uid: UUID,
)-> CategoriesResponseSchema:
  async with ModelRepository[CategoriesModel](db, CategoriesModel) as repo:
    categories = await repo.create({**body.model_dump(), 'user_uid': user_uid })
  return CategoriesResponseSchema.model_validate(categories)


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


async def get_all_service(
    db: AsyncSession
):
  pass
