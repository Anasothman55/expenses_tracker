from uuid import UUID, uuid7
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Text, Enum as SqlEnum, UUID as SqlUUID, TIMESTAMP

from app.shared.utils.constant import PROJECT_DATETIME


class Base(DeclarativeBase):
  pass


class EssentialColumnValidation(BaseModel):
  uid: UUID
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None = None


class EssentialColumns(Base):
  __abstract__ = True

  uid: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, index=True, default=lambda _: uuid7())
  created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False),
    default=PROJECT_DATETIME.get_datetime,
    nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False),
    default=PROJECT_DATETIME.get_datetime,
    onupdate=PROJECT_DATETIME.get_datetime,
    nullable=False
  )
  deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=False),default=None,nullable=True)

  def set_soft_delete(self):
    self.deleted_at = PROJECT_DATETIME.get_datetime()
















