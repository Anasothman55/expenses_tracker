from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession



async def create_service(
    body: str,
    db: AsyncSession
):
  pass


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
