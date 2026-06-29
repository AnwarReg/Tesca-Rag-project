from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, loaded from environment variables (or a .env file)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    gemini_api_key: str

    # Clerk — optional so local dev (with the bypass below) needs no Clerk setup.
    clerk_jwks_url: str | None = None
    clerk_issuer: str | None = None

    # Dev-only: skip JWT validation and treat every request as `dev_user_id`.
    # Never enable in production.
    dev_auth_bypass: bool = False
    dev_user_id: str = "dev-user"

    s3_bucket: str | None = None
    aws_region: str = "us-east-1"


settings = Settings()
