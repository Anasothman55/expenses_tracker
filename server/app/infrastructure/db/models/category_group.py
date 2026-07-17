from uuid import UUID
from pydantic import Field, StringConstraints, ConfigDict
from typing import  Annotated

from sqlalchemy import String, CHAR, UUID as SqlUUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base import EssentialColumns, EssentialColumnValidation

CategoryGroupName = Annotated[str,StringConstraints(min_length=3,max_length=64,strip_whitespace=True,), Field(examples=["Housing"]),]
CategoryGroupRgbColor = Annotated[str,StringConstraints(min_length=3,max_length=3,strip_whitespace=True,pattern=r"^[0-9A-Fa-f]{6}$"), Field(examples=["64748B"]),]
CategoryGroupIcons = Annotated[str, Field(..., max_length=255, examples=['image/icon/house.svg'])]


class CategoryGroupModelValidation(EssentialColumnValidation):
  name: CategoryGroupName
  rgb_color: CategoryGroupRgbColor
  icons: CategoryGroupIcons

  user_uid: UUID

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class CategoryGroupModel(EssentialColumns):
  __tablename__ = 'category_group'

  name: Mapped[str] = mapped_column(String(64), nullable=False)
  rgb_color: Mapped[str] = mapped_column(CHAR(3), nullable=False, default='64748B')
  icons: Mapped[str | None] = mapped_column(String(255), nullable=True,)

  user_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)

  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> CategoryGroupModelValidation:
    return CategoryGroupModelValidation.model_validate(self)

  __table_args__ = (
    UniqueConstraint('user_uid', 'name', name='user_uid_name'),
  )










