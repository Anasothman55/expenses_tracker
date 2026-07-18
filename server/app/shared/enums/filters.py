from enum import StrEnum


class FilterOperator(StrEnum):
  eq = "eq"
  ne = "ne"
  lt = "lt"
  lte = "lte"
  gt = "gt"
  gte = "gte"
  contains = "contains"
  between = "between"