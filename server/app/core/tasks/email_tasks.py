from loguru import logger

from app.core.celery_app import celery_app
from app.core.tasks.base import BaseTask
from app.infrastructure.email.renderer import render_template
from app.infrastructure.email.client import send_email




@celery_app.task(
  bind= True,
  base= BaseTask,
  name= "tasks.send_welcome_email",
  ignore_result= True,
  max_retries= 3,
  default_retry_delay= 60,
)
def send_welcome_email_task(self, to_email: str, name: str)-> None:
  try:
    html = render_template("welcome.html", {"name": name})
    send_email(
      to_email=to_email,
      subject="Welcome to MyApp!",
      html_body=html,
    )
  except Exception as exc:
    logger.error(f"Failed to send welcome email to {to_email}: {exc}")
    raise self.retry(exc=exc)


@celery_app.task(
  bind= True,
  base= BaseTask,
  name= "tasks.send_verify_email",
  ignore_result= True,
  max_retries= 3,
  default_retry_delay= 60,
)
def send_verify_email_task(self, to_email: str, context: dict)-> None:
  try:
    html = render_template("verify_email.html", context)
    send_email(
      to_email=to_email,
      subject="Email Address Verification",
      html_body=html,
    )
  except Exception as exc:
    logger.error(f"Failed to send verification email to {to_email}: {exc}")
    raise self.retry(exc=exc)

@celery_app.task(
  bind= True,
  base= BaseTask,
  name= "tasks.send_password_reset_email",
  ignore_result= True,
  max_retries= 3,
  default_retry_delay= 60,
)
def send_password_reset_email_task(self, to_email: str, context: dict)-> None:
  try:
    html = render_template('reset_password.html', context)
    send_email(
      to_email=to_email,
      subject="Reset Password",
      html_body=html,
    )
  except Exception as exc:
    logger.error(f"Failed to send password reset email to {to_email}: {exc}")
    raise self.retry(exc=exc)


