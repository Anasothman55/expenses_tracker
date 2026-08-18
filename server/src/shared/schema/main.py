from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
  health: bool
  status: str
  message: str





