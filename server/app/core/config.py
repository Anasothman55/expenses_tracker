from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):

  LOG_LEVEL: str
  LOG_JSON: bool

  # SERVER
  SERVER_PORT: int = 8000
  SERVER_HOST: str
  SERVER_WORKER: int
  DEVELOP_MODE: bool

  #LIMITER
  DEFAULT_LIMITER: List[str]

  # DATABASE
  DATABASE_USERNAME: str
  DATABASE_PASSWORD: SecretStr
  DATABASE_HOST: str
  DATABASE_PORT: int
  DATABASE_NAME: str

  def db_url(self) -> str:
    return f"postgresql+psycopg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD.get_secret_value()}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

  REDIS_HOST: str
  REDIS_PORT: int = 6379
  REDIS_USERNAME: str | None = None
  REDIS_PASSWORD: str | None = None
  REDIS_DB: int = 0

  REDIS_REFRESH_JTI: str

  def REDIS_REFRESH_TOKEN_EXPIRE(self) -> int:
    return self.JWT_REFRESH_TOKEN_EXPIRE

  def redis_url(self, redis_db: int = 0) ->  str:
    return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{redis_db}"

  # celery
  def CELERY_BROKER_URL(self)-> str: return self.redis_url(redis_db=1)
  def CELERY_RESULT_BACKEND(self)-> str: return self.redis_url(redis_db=2)

  # JWT
  JWT_SECRET_KEY: SecretStr
  JWT_ALGORITHM: str
  JWT_ACCESS_TOKEN_EXPIRE_MINUTE: int
  JWT_ACCESS_TOKEN_EXPIRE_DAYS: int
  JWT_REFRESH_TOKEN_EXPIRE: int

  # TOKEN
  # ADMIN_TOKEN_KEY=''
  # USER_TOKEN_KEY=''

  # PASSWORD SECRET
  PASSWORD_SECRET: SecretStr

  # CORS
  # CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:51

  # Utils
  TIME_ZONE: bool

  # Email sender detail
  SMTP_HOST: str
  SMTP_PORT: int
  SMTP_USER: str
  SMTP_PASSWORD: str
  EMAILS_FROM_EMAIL: str
  EMAILS_FROM_NAME: str

  EMAIL_VERIFY_TOKEN_SECRET_KEY: SecretStr
  EMAIL_VERIFY_TOKEN_SECRET_SALT: SecretStr

  ACCESS_TOKEN_COOKIE_NAME: str
  REFRESH_TOKEN_COOKIE_NAME: str
  def COOKIE_MAX_AGE(self) -> int:
    return self.JWT_REFRESH_TOKEN_EXPIRE

  # Email reset
  PASSWORD_RESET_OTP_KEY: SecretStr

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )



settings = Settings() # type: ignore








