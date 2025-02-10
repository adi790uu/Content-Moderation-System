import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SYNC_DATABASE_URL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    REDIS_URL: Optional[str] = None


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
