from typing import List, Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.currencies import CurrenciesModelValidation
from app.modules.currencies.schema import CurrenciesCreateSchema
from app.modules.currencies.service import get_currencies_service, post_currencies_service
from app.core.deps.db import get_db
from app.modules.auth.deps import get_current_user


currencies_route = APIRouter(
  tags=["Currencies"],
  dependencies=[Depends(get_current_user)]
)

@currencies_route.post("/", response_model=CurrenciesModelValidation, status_code=status.HTTP_201_CREATED, deprecated=True)
async def get_currencies(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: CurrenciesCreateSchema,
):
  return await post_currencies_service(db, body)



@currencies_route.get("/", response_model=List[CurrenciesModelValidation])
async def get_currencies(
    db: Annotated[AsyncSession, Depends(get_db)]
):
  return await get_currencies_service(db)

