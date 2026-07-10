from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

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
        env_file=".env",
        env_file_encoding="utf-8"
)

#Instantiate configuration
settings = Settings()
print(settings)