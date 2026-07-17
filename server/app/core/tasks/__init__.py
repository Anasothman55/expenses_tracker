from loguru import logger

from app.core.celery_app import celery_app
from app.core.tasks.base import BaseTask
from app.infrastructure.email.renderer import render_template
from app.infrastructure.email.client import send_email

@celery_app.task(
  bind= True,
  base= BaseTask,
  name= "tasks.ping",
)
def ping(self, message: str)-> str:
  logger.info(f"Ping Task executed Ping: {message}")
  return message



