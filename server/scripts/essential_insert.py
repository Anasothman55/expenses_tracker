from rich import print

from sqlalchemy import insert

from src.infrastructure.db.engine import SessionLocal
from src.infrastructure.db.models import CurrenciesModel
from src.modules.currencies.api import currency_crud, CurrenciesCreateSchema



async def main():

  async with SessionLocal() as session:
    to_insert: list[CurrenciesCreateSchema] = [
      CurrenciesCreateSchema(name='EU Euro', symbol='€', code='EUR').model_dump(),
      CurrenciesCreateSchema(name='US Dollar', symbol='$', code='USD').model_dump(),
      CurrenciesCreateSchema(name='Iraq Dinar', symbol='د.ع', code='IQD').model_dump(),
    ]

    await session.execute(
      insert(CurrenciesModel),
      to_insert
    )
    await session.commit()
    print({
      "message": "Currencies successfully created",
      "data": to_insert
    })


