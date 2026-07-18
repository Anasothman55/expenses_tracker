from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError

from fastapi import Query, Depends

from app.infrastructure.db.models.category_group import CategoryGroupModelValidation
from app.infrastructure.db.models.category_group import (
  CategoryGroupName,
  CategoryGroupRgbColor,
  CategoryGroupIcons,
)
from app.shared.enums.filters import FilterOperator


# body

class CategoryGroupCreateSchema(BaseModel):
  name: CategoryGroupName
  rgb_color: CategoryGroupRgbColor
  icons: CategoryGroupIcons | None = None

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )


# response model

class CategoryGroupResponseAllSchema(CategoryGroupModelValidation):
  pass

# query params

class CategoryGroupQueryAll(BaseModel):
  is_pagination: Annotated[bool, Query(default=False)]
  include_deleted: Annotated[bool, Query(default=False)]

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='forbid'
  )


# filter query

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