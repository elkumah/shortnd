import json
import os
from functools import cached_property

import boto3
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

ENV_FILE = os.getenv("ENV_FILE", ".env")


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    BASE_URL: str

    AWS_REGION: str = "us-east-1"
    AWS_SECRET_ARN: str | None = None

    # Used for local development and testing.
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None

    @cached_property
    def database_credentials(self) -> dict[str, str]:
        """Load credentials from AWS Secrets Manager or local settings."""

        if self.AWS_SECRET_ARN:
            client = boto3.client(
                "secretsmanager",
                region_name=self.AWS_REGION,
            )

            response = client.get_secret_value(
                SecretId=self.AWS_SECRET_ARN,
            )

            secret_string = response.get("SecretString")
            if not secret_string:
                raise ValueError(
                    "The configured RDS secret does not contain SecretString."
                )

            secret = json.loads(secret_string)

            username = secret.get("username")
            password = secret.get("password")

            if not username or not password:
                raise ValueError(
                    "The RDS secret must contain username and password fields."
                )

            return {
                "username": username,
                "password": password,
            }

        if self.POSTGRES_USER and self.POSTGRES_PASSWORD:
            return {
                "username": self.POSTGRES_USER,
                "password": self.POSTGRES_PASSWORD,
            }

        raise ValueError(
            "Configure AWS_SECRET_ARN for AWS deployments, or set "
            "POSTGRES_USER and POSTGRES_PASSWORD for local development."
        )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Build the SQLAlchemy database URL."""

        credentials = self.database_credentials

        database_url = URL.create(
            drivername="postgresql",
            username=credentials["username"],
            password=credentials["password"],
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )

        return database_url.render_as_string(hide_password=False)


settings = Settings()

