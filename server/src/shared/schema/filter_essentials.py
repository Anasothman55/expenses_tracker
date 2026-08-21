from pydantic import BaseModel, Field, ConfigDict


class FilterEssentials(BaseModel):
  offset: int | None = Field(None, ge=0)
  limit: int | None = Field(None, ge=1, le=100)

  page: int = Field(None, ge=1)
  items_per_page: int = Field(None, ge=1, le=100)

  sort_columns: list[str] | None = None
  sort_orders: list[str] | None = None

  include_deleted: bool | None = False

  model_config = ConfigDict(
    extra='forbid'
  )





