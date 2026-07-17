from datetime import datetime, timedelta, timezone, time, date
from dataclasses import dataclass, field
from typing import Final

from app.core.config import settings


@dataclass()
class Timestamp:
  time_zone: bool = field(default=False)

  def get_datetime(self) -> datetime:
    if self.time_zone:
      return datetime.now(timezone.utc)
    return datetime.now()

  def get_time(self) -> time:
    return self.get_datetime().time()

  def get_date(self) -> date:
    return self.get_datetime().date()


PROJECT_DATETIME: Final[Timestamp] = Timestamp(time_zone=settings.TIME_ZONE)

if __name__ == "__main__":
  print("Current DateTime:", PROJECT_DATETIME.get_datetime())
  print("Current Time:", PROJECT_DATETIME.get_time())
  print("Current Date:", PROJECT_DATETIME.get_date())




