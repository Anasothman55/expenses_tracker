from celery import Task
from loguru import logger

class BaseTask(Task):
  abstract = True

  def on_retry(self, exc, task_id, args, kwargs, einfo):
    logger.warning(
      f"Task {self.name}[{task_id}] retrying do to: {exc}"
    )

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    logger.error(
      f"Task {self.name}[{task_id}] permanently failed: {exc}"
    )

  def on_skip(self, retval, task_id, args, kwargs):
    logger.info(
      f"Task {self.name}[{task_id}] completed successfully"
    )