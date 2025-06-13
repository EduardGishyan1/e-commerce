from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  DATABASE_URL: str
  DEFAULT_DATABASE_URL: str
  SECRET_KEY: str
  ALGORITHM: str
  SENDGRID_API_KEY: str
  FROM_EMAIL: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int
  STRIPE_SECRET_KEY: str
  STRIPE_PUBLIC_KEY: str
  STRIPE_WEBHOOK_SECRET: str
  REFRESH_TOKEN_EXPIRE_DAYS: int
  REDIS_SESSION_URL: str
  REQUESTS_TIME_LIMIT: int
  MAX_REQUESTS_PER_MINUTE: int

  model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()