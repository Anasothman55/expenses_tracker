from celery import Celery

from app.core.config import settings

celery_app = Celery(
  "app",
  broker=settings.CELERY_BROKER_URL(),
  backend=settings.CELERY_RESULT_BACKEND(),
)

celery_app.conf.update(
  # Serialization
  task_serializer="json",
  result_serializer="json",
  accept_content=["json"],

  # Reliability
  task_acks_late=True,            # ack only after tasks finishes
  task_reject_on_worker_lost=True, # re-queue if worker dies mid-tasks
  worker_prefetch_multiplier=1,   # one tasks at a time per worker slot

  # Retries
  task_default_retry_delay=30,    # seconds before retry
  task_max_retries=3,

  # Results
  result_expires=3600,            # keep results in Redis for 1 hour

  # Timezone
  timezone="UTC",
  enable_utc=True,
)

celery_app.autodiscover_tasks(["app.tasks"])












