import hmac
import hashlib

from pydantic import BaseModel

from app.core.config import settings


class OtpData(BaseModel):
  user_uid: str
  otp_hash: str
  expires_at: int
  created_at: int
  attempt_count: int

def otp_decoded(otp: str)-> str:
  return hmac.new(
    settings.PASSWORD_RESET_OTP_KEY.get_secret_value().encode(),
    otp.encode(),
    hashlib.sha256
  ).hexdigest()

def otp_verify(stored_hash: str, submitted_hash: str) -> bool:
  return hmac.compare_digest(stored_hash, submitted_hash)




