from typing import List, Annotated

from fastapi import APIRouter, Depends, status
from fastcrud import FastCRUD, EndpointCreator
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.currencies.schema import CurrenciesCreateSchema, CurrenciesResponseSchema, CurrenciesUpdateSchema
from src.modules.currencies.service import get_currencies_service, post_currencies_service
from src.core.deps.db import get_db
from src.modules.auth.deps import get_current_user
from src.infrastructure.db.models.currencies import CurrenciesModel, CurrenciesModelValidation

currency_crud = FastCRUD(CurrenciesModel)


endpoint_currency = EndpointCreator(
  session=get_db,
  model=CurrenciesModel,
  crud=currency_crud,
  tags=["Currency"],
  create_schema=CurrenciesCreateSchema,
  update_schema=CurrenciesUpdateSchema,
  select_schema=CurrenciesResponseSchema,
)

endpoint_currency.add_routes_to_router(
  included_methods=[
    "read",
    "read_multi",
  ],
  read_deps=[get_current_user],
  read_multi_deps=[get_current_user]
)



# currencies_route = APIRouter(
#   tags=["Currencies"],
#   dependencies=[Depends(get_current_user)]
# )
#
# @currencies_route.post("/", response_model=CurrenciesModelValidation, status_code=status.HTTP_201_CREATED, deprecated=True)
# async def get_currencies(
#     db: Annotated[AsyncSession, Depends(get_db)],
#     body: CurrenciesCreateSchema,
# ):
#   return await post_currencies_service(db, body)
#
#
#
# @currencies_route.get("/", response_model=List[CurrenciesModelValidation])
# async def get_currencies(
#     db: Annotated[AsyncSession, Depends(get_db)]
# ):
#   return await get_currencies_service(db)

