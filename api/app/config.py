import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env")
class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    # Application settings loaded from environment variables
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    BASE_URL: str  # Base URL for the application, e.g., http://localhost:8000

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8"
)

#Instantiate configuration
settings = Settings()
print(settings)