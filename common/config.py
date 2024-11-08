"""
Настройки конфигурации приложения, такие как параметры подключения
к базе данных, секретные ключи и прочие настройки.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from enum import Enum


class ModeEnum(str, Enum):
    dev = "dev"
    prod = "prod"
    test = "test"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings():
    return Settings().model_dump()


settings = get_settings()
# print(settings["db_url_test"])
# print(settings["mode"])
