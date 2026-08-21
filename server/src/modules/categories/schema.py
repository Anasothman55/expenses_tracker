from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from src.infrastructure.db.base import EssentialColumnValidation
from src.shared.schema.read_multi_essential import ReadMultiEssential
from src.shared.schema.filter_essentials import FilterEssentials
from src.shared.utils.fastcrud_filter import create_filter
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
  icons: CategoriesIcons | None = None
  is_transfer: CategoriesIsTransfer = False
  group_uid: UUID | None = None

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

class CategoriesResponseSchema(CategoriesCreateSchema, EssentialColumnValidation):
  pass

class CategoriesReadMultiResponse(ReadMultiEssential):
  data: list[CategoriesResponseSchema]

class CategoriesReadResponse(CategoriesCreateSchema):
  pass

# filter

NameFilter = create_filter('name', {"eq":True, "ilike":True, 'in':True}, str)
Created_atFilter = create_filter('created_at', {"lte":True, "gte":True, 'between': True}, datetime)

class CategoriesReadMultiFilter(NameFilter, Created_atFilter, FilterEssentials):

  @classmethod
  def preprocess(cls, data: dict) -> dict:
    filters = {}

    for k, v in data.items():
      if k.startswith("name__"):
        filters[k] = v

      elif k.startswith("created_at__"):
        filters[k] = v

    return filters










