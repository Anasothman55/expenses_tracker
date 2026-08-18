from typing import TypedDict, Any


class ExceptionDetails(TypedDict):
  loc: list[str]
  msg: str
  type: str
  input: Any | None










