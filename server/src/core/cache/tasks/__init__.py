from loguru import logger

from src.core.cache.celery_app import celery_app
from src.core.cache.tasks.base import BaseTask
from src.infrastructure.email.renderer import render_template
from src.infrastructure.email.client import send_email

@celery_app.task(
  bind= True,
  base= BaseTask,
  name= "tasks.ping",
)
def ping(self, message: str)-> str:
  logger.info(f"Ping Task executed Ping: {message}")
  return message



