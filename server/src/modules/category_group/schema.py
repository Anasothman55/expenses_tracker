from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError, field_validator
import json

from fastapi import Query, Depends

from src.shared.schema.read_multi_essential import ReadMultiEssential
from src.shared.utils.fastcrud_filter import create_filter
from src.shared.schema.filter_essentials import FilterEssentials
from src.shared.utils.fastcrud_filter import FilterType,FilterTypeDict
from src.modules.categories.schema import CategoriesResponseSchema
from src.infrastructure.db.models.category_group import CategoryGroupModelValidation
from src.infrastructure.db.models.category_group import (
  CategoryGroupName,
  CategoryGroupRgbColor,
  CategoryGroupIcons,
)
from src.shared.enums.filters import FilterOperator


# body

class CategoryGroupCreateSchema(BaseModel):
  name: CategoryGroupName
  rgb_color: CategoryGroupRgbColor
  icons: CategoryGroupIcons | None = None

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )

class CategoryGroupUpdateSchema(BaseModel):
  name: CategoryGroupName | None = None
  rgb_color: CategoryGroupRgbColor | None = None
  icons: CategoryGroupIcons | None = None

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )


# response model

class CategoryGroupResponseAllSchema(CategoryGroupModelValidation):
  pass

class CategoryGroupReadMultiResponse(ReadMultiEssential):
  data: list[CategoryGroupResponseAllSchema]

class CategoryGroupResponseSchema(CategoryGroupModelValidation):
  categories: list[CategoriesResponseSchema] | None = None

# query params

class CategoryGroupQueryAll(BaseModel):
  is_pagination: Annotated[bool, Query(default=False)]
  include_deleted: Annotated[bool, Query(default=False)]

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )


# filter query

NameFilter = create_filter('name', {"eq":True, "ilike":True, 'in':True}, str)
Created_atFilter = create_filter('created_at', {"lte":True, "gte":True, 'between': True}, datetime)

class CategoryGroupReadMultiFilter(FilterEssentials, NameFilter, Created_atFilter):

  @classmethod
  def preprocess(cls, data: dict) -> dict:
    filters = {}

    for k, v in data.items():
      if k.startswith("name__"):
        filters[k] = v

      elif k.startswith("created_at__"):
        filters[k] = v

    return filters


class CategoryGroupColumn(StrEnum):
  created_at = 'created_at'
  updated_at = 'updated_at'
  deleted_at = 'deleted_at'
  name = 'name'
  rgb_color = 'rgb_color'
  icons = 'icons'


class CategoryGroupFilterAll(BaseModel):
  column: CategoryGroupColumn
  operator: FilterOperator
  value: Any

  @model_validator(mode='after')
  def validation_model(self):
    date_columns = {
      CategoryGroupColumn.created_at,
      CategoryGroupColumn.updated_at,
      CategoryGroupColumn.deleted_at,
    }

    if self.column in date_columns and self.value:
      values_to_check = self.value if isinstance(self.value, list) else [self.value]
      parsed = []
      for v in values_to_check:
        try:
          parsed.append(datetime.fromisoformat(v))
        except Exception as e:
          raise ValueError(f"Invalid date value for {self.column}: {v}") from e
      self.value = parsed if isinstance(self.value, list) else parsed[0]

    if self.operator == FilterOperator.between:
      if not isinstance(self.value, list) or len(self.value) != 2:
        raise ValueError("'between' operator requires exactly 2 values")

    return self


  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )