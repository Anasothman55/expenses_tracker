from pydantic import BaseModel


class ReadMultiEssential(BaseModel):
  total_count: int
  has_more: bool
  page: int
  items_per_page: int

