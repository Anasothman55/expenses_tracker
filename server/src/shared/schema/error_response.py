from typing import Any, Sequence

from pydantic import BaseModel


class ErrorResponse(BaseModel):
  status_code: int
  error_code: str
  message: str
  detail: Sequence[Any] | None = None








