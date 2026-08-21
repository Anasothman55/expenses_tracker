from uuid import UUID

from pydantic import EmailStr, Field, StringConstraints, BaseModel, StrictBool, ConfigDict
from typing import Optional, Annotated

from sqlalchemy import Text, String, Boolean, Index, text, UUID as SqlUUID, ForeignKey, CHAR, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, EssentialColumns, EssentialColumnValidation

CategoriesName = Annotated[str,StringConstraints(min_length=3,max_length=64,strip_whitespace=True,), Field(examples=["Rent"]),]
CategoriesRgbColor = Annotated[str,StringConstraints(min_length=6,max_length=6,strip_whitespace=True,pattern=r"^[0-9A-Fa-f]{6}$"), Field(examples=["64748B"]),]
CategoriesIcons = Annotated[str, Field(..., max_length=255, examples=['image/icon/house.svg'])]
CategoriesIsTransfer = Annotated[bool, StrictBool, Field(...)]



class CategoriesModelValidation(EssentialColumnValidation):
  name: CategoriesName
  rgb_color: CategoriesRgbColor
  icons: CategoriesIcons | None = None
  is_transfer: CategoriesIsTransfer

  user_uid: UUID
  group_uid: UUID | None = None

  model_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
  )

class CategoriesModel(EssentialColumns):
  __tablename__ = 'categories'

  name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
  rgb_color: Mapped[str] = mapped_column(CHAR(6), nullable=False, default='64748B')
  icons: Mapped[str | None] = mapped_column(String(255), nullable=True,)
  is_transfer: Mapped[bool] = mapped_column(Boolean(), default=False)

  user_uid: Mapped[UUID] = mapped_column(SqlUUID, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
  group_uid: Mapped[UUID | None] = mapped_column(SqlUUID, ForeignKey('category_group.uid', ondelete='SET NULL') ,nullable=True, default=None)
  group: Mapped['CategoryGroupModel | None'] = relationship(
    "CategoryGroupModel",
    remote_side="CategoryGroupModel.uid",
    foreign_keys=[group_uid],
    back_populates="categories",
    lazy="select"
  )

  def set_soft_delete(self):
    super().set_soft_delete()

  def validate(self) -> CategoriesModelValidation:
    return CategoriesModelValidation.model_validate(self)

  __table_args__ = (
    UniqueConstraint( 'name', 'user_uid', name='group_uid_name_user_uid'),
  )












