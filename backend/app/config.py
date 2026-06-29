from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, loaded from environment variables (or a .env file)."""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    clerk_jwks_url: str
    clerk_issuer: str


settings = Settings()
