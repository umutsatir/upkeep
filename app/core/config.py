# OWNER: MEMBER-1
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "upkeep"
    app_env: str = "development"
    secret_key: str = "change-me-in-production"


settings = Settings()
