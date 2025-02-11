import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_URL: Optional[str] = None
    MODERATION_SERVICE_BASE_URL: Optional[str] = "http://localhost:8001"
    GATEWAY_KEY: Optional[str] = "secret"


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.development")


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.test")


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.production")


def get_settings() -> Settings:
    if os.getenv("APP_ENV", "development") == "production":
        return ProductionSettings()
    elif os.getenv("APP_ENV", "development") == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()
