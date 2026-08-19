from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.infrastructure.db.models.categories import (
  CategoriesModelValidation,
  CategoriesName,
  CategoriesRgbColor,
  CategoriesIcons,
  CategoriesIsTransfer,
)


# body schema
class CategoriesCreateSchema(BaseModel):

  name: CategoriesName
  rgb_color: CategoriesRgbColor
  icons: CategoriesIcons
  is_transfer: CategoriesIsTransfer = False
  group_uid: UUID | None = Field(None, exclude=True)

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid"
  )

class CategoriesUpdateSchema(BaseModel):
  name: CategoriesName | None = None
  rgb_color: CategoriesRgbColor | None = None
  icons: CategoriesIcons | None = None
  is_transfer: CategoriesIsTransfer | None = None
  group_uid: UUID | None = None

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid"
  )


# response

class CategoriesResponseSchema(CategoriesCreateSchema):
  pass












