from pydantic import EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from loguru import logger
from app.core.config import settings



def send_email(
    to_email: EmailStr,
    subject: str,
    html_body: str
):
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
  msg['To'] = to_email

  msg.attach(MIMEText(html_body, 'html'))

  with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    smtp.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())
    logger.info(f"Email sent to {to_email}")










