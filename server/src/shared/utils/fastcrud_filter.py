from typing import TypedDict, NotRequired, Any

from pydantic import BaseModel, ConfigDict, create_model
from datetime import datetime, time, date
from decimal import Decimal



FilterTypeDict = TypedDict(
  "FilterTypeDict",
  {
    "eq": NotRequired[bool],
    "ne": NotRequired[bool],
    "gt": NotRequired[bool],
    "lt": NotRequired[bool],
    "gte": NotRequired[bool],
    "lte": NotRequired[bool],
    "in": NotRequired[bool],
    "not_in": NotRequired[bool],
    "between": NotRequired[bool],
    "like": NotRequired[bool],
    "ilike": NotRequired[bool],
    "startswith": NotRequired[bool],
    "endswith": NotRequired[bool],
    "contains": NotRequired[bool],
    "is": NotRequired[bool],
    "is_not": NotRequired[bool],
  },
)


Comparison = int | float | datetime | date | time | Decimal

class FilterType(BaseModel):
  model_config = ConfigDict(populate_by_name=True, extra="forbid")

  eq: Any | None = None
  ne: Any | None = None
  gt:  Comparison | None = None
  lt:  Comparison | None = None
  gte: Comparison | None = None
  lte: Comparison | None = None

  not_in: list[Any] | None = None

  between: tuple[Comparison, Comparison] | None = None

  like: str | None = None
  ilike: str | None = None
  startswith: str | None = None
  endswith: str | None = None
  contains: str | None = None

  is_not: bool | None = None
  in_value: list[Any] | None = None
  is_value: bool | None = None



def create_filter[T](
    column: str,
    filter_by: FilterTypeDict,
    field_type: type[T],
) -> type[BaseModel]:

  result = column[:1].upper() + column[1:]
  fields = {}

  for name in filter_by:
    field_name = f"{column}__{name}"

    if name in {"eq", "ne", "gt", "lt", "gte", "lte"}:
        annotation = field_type | None

    elif name in {"in", "not_in"}:
        annotation = list[field_type] | None # type: ignore[valid-type]

    elif name == "between":
        annotation = tuple[field_type, field_type] | None # type: ignore[valid-type]

    elif name in {"like", "ilike", "startswith", "endswith", "contains"}:
        annotation = str | None

    elif name in {"is", "is_not"}:
        annotation = bool | None

    else:
        raise ValueError(f"Unknown filter: {name}")

    fields[field_name] = (annotation, None)

  return create_model(f"{result}Filter", **fields)
