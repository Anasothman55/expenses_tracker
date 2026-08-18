from .schema import CategoryGroupFilterAll
from fastapi import Query, HTTPException

def parse_category_group_filters(
    filters: list[str] | None = Query(
      default=None,
      description="format: column:operator:value, e.g. name:contains:a",
    ),
) -> list[CategoryGroupFilterAll]:
  if not filters:
    return []

  parsed: list[CategoryGroupFilterAll] = []
  for raw in filters:
    try:
      column, operator, value = raw.split(":", 2)
    except ValueError:
      raise HTTPException(400, f"Invalid filter format: '{raw}'")

    if operator == "between":
      value = value.strip("[]").split(",")
      value = [v.strip() for v in value]
    parsed.append(
      CategoryGroupFilterAll(column=column, operator=operator, value=value)
    )
  return parsed