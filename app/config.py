import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='APP_', extra="allow")
    db_url: str


def acquire_app_config() -> AppConfig:
    environment = os.getenv("APP_ENVIRONMENT", "")
    return AppConfig(_env_file=f"{environment}.env")
