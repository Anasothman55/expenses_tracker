from sqlalchemy import and_

OPERATORS = {
  "eq": lambda c, v: c == v,
  "ne": lambda c, v: c != v,
  "lt": lambda c, v: c < v,
  "lte": lambda c, v: c <= v,
  "gt": lambda c, v: c > v,
  "gte": lambda c, v: c >= v,
  "contains": lambda c, v: c.contains(v),
  "between": lambda c, v: c.between(v[0], v[1]),
}