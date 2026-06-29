from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, loaded from environment variables (or a .env file)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    clerk_jwks_url: str
    clerk_issuer: str
    gemini_api_key: str
    s3_bucket: str | None = None
    aws_region: str = "us-east-1"


settings = Settings()
