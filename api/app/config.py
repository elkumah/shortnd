import json
import os
from functools import cached_property

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pydantic import SecretStr, computed_field
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

    # Database connection settings
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Application settings
    BASE_URL: str

    # AWS configuration
    AWS_REGION: str = "us-east-1"
    AWS_SECRET_ARN: str | None = None

    # Local development and CI credentials
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: SecretStr | None = None

    @cached_property
    def database_credentials(self) -> dict[str, str]:
        """Retrieve database credentials from AWS Secrets Manager or local environment."""

        if self.AWS_SECRET_ARN:
            return self._get_aws_database_credentials()

        if self.POSTGRES_USER and self.POSTGRES_PASSWORD:
            return {
                "username": self.POSTGRES_USER,
                "password": self.POSTGRES_PASSWORD.get_secret_value(),
            }

        raise ValueError(
            "Configure AWS_SECRET_ARN for AWS deployments, or set "
            "POSTGRES_USER and POSTGRES_PASSWORD for local development."
        )

    def _get_aws_database_credentials(self) -> dict[str, str]:
        """Retrieve database credentials from AWS Secrets Manager."""

        try:
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

        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(
                "Unable to retrieve database credentials from AWS Secrets Manager."
            ) from exc

        except json.JSONDecodeError as exc:
            raise ValueError(
                "The configured RDS secret contains invalid JSON."
            ) from exc

    @computed_field
    @cached_property
    def DATABASE_URL(self) -> URL:
        """Build a SQLAlchemy URL without rendering credentials into plaintext."""

        credentials = self.database_credentials

        return URL.create(
            drivername="postgresql+psycopg2",
            username=credentials["username"],
            password=credentials["password"],
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings()
