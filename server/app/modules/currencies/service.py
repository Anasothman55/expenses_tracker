from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.currencies import CurrenciesModelValidation, CurrenciesModel
from app.modules.currencies.schema import CurrenciesCreateSchema
from app.shared.utils.model_repository import ModelRepository


async def post_currencies_service(
  db: AsyncSession,
  body: CurrenciesCreateSchema
)-> CurrenciesModel:
  async with ModelRepository[CurrenciesModel](db, CurrenciesModel) as repo:
    return await repo.create(body)

async def get_currencies_service(
    db: AsyncSession,
) -> Sequence[CurrenciesModel]:
  async with ModelRepository[CurrenciesModel](db, CurrenciesModel) as repo:
    return await repo.get_all(False, False, None, None)