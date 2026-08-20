from enum import StrEnum
from typing import TypedDict, NotRequired

from fastapi.openapi import docs

class FilterType(TypedDict):
  eq_: NotRequired[bool | None]
  ne_: NotRequired[bool | None]
  gt_: NotRequired[bool | None]
  lt_: NotRequired[bool | None]
  gte_: NotRequired[bool | None]
  lte_: NotRequired[bool | None]
  in_: NotRequired[bool | None]
  not_in_: NotRequired[bool | None]
  between_: NotRequired[bool | None]
  like_: NotRequired[bool | None]
  ilike_: NotRequired[bool | None]
  startswith_: NotRequired[bool | None]
  endswith_: NotRequired[bool | None]
  contains_: NotRequired[bool | None]
  is_: NotRequired[bool | None]
  is_not_: NotRequired[bool | None]
  not_: NotRequired[bool | None]

def add_filter(
    column: str,
    filter_by: FilterType,
) -> dict:
  """
  __eq	equals (same as no suffix)
  __ne	not equal
  __gt	greater than
  __lt	less than
  __gte	greater than or equal
  __lte	less than or equal
  __in	value in a list
  __not_in	value not in a list
  __between	between two values (range)
  __like	SQL LIKE (case-sensitive pattern match)
  __ilike	case-insensitive LIKE
  __startswith	starts with
  __endswith	ends with
  __contains	contains substring
  __is	IS (for boolean/null checks)
  __is_not	IS NOT
  __or	OR group of sub-operators on the same field
  __not	NOT group of sub-operators on the same field

  """

  return {
    f"{column}__{k}".rstrip("_"): None  for k, v in filter_by.items() if v == True
  }
