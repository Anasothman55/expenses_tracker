from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.engine import SessionLocal


async def get_db()-> AsyncGenerator[AsyncSession, None]:
  async with SessionLocal() as session:
    try:
      yield session
    except  Exception as e:
      await session.rollback()
      raise
