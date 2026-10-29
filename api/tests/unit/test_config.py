
import json
from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings


@pytest.fixture
def base_settings():
    """Provide the minimum configuration required for Settings."""
    return {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": 5432,
        "POSTGRES_DB": "shortnd_test",
        "BASE_URL": "http://localhost:8000",
    }


def test_database_credentials_from_environment(base_settings):
    """Use local credentials when AWS Secrets Manager is not configured."""
    settings = Settings(
        **base_settings,
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
    )

    assert settings.database_credentials == {
        "username": "test_user",
        "password": "test_password",
    }


@patch("app.config.boto3.client")
def test_database_credentials_from_secrets_manager(
    mock_boto_client, base_settings
):
    """Retrieve database credentials from AWS Secrets Manager."""
    mock_client = MagicMock()
    mock_boto_client.return_value = mock_client
    mock_client.get_secret_value.return_value = {
        "SecretString": json.dumps(
            {
                "username": "shortnd_admin",
                "password": "test_secret_password",
            }
        )
    }

    settings = Settings(
        **base_settings,
        AWS_REGION="us-east-1",
        AWS_SECRET_ARN="arn:aws:secretsmanager:us-east-1:123456789012:secret:test",
    )

    assert settings.database_credentials == {
        "username": "shortnd_admin",
        "password": "test_secret_password",
    }

    mock_boto_client.assert_called_once_with(
        "secretsmanager",
        region_name="us-east-1",
    )
    mock_client.get_secret_value.assert_called_once_with(
        SecretId=settings.AWS_SECRET_ARN
    )


@pytest.mark.parametrize("secret_response", [{}, {"SecretString": ""}, {"SecretString": None}])
@patch("app.config.boto3.client")
def test_missing_secret_string_raises_value_error(
    mock_boto_client, secret_response, base_settings
):
    """Reject a Secrets Manager response without SecretString."""
    mock_client = MagicMock()
    mock_boto_client.return_value = mock_client
    mock_client.get_secret_value.return_value = secret_response

    settings = Settings(
        **base_settings,
        AWS_SECRET_ARN="test-secret-arn",
    )

    with pytest.raises(ValueError, match="does not contain SecretString"):
        _ = settings.database_credentials


@pytest.mark.parametrize(
    "secret",
    [
        {},
        {"username": "shortnd_admin"},
        {"password": "test_password"},
        {"username": "", "password": "test_password"},
        {"username": "shortnd_admin", "password": ""},
    ],
)
@patch("app.config.boto3.client")
def test_invalid_secret_credentials_raise_value_error(
    mock_boto_client, secret, base_settings
):
    """Reject secrets without both a username and password."""
    mock_client = MagicMock()
    mock_boto_client.return_value = mock_client
    mock_client.get_secret_value.return_value = {
        "SecretString": json.dumps(secret)
    }

    settings = Settings(
        **base_settings,
        AWS_SECRET_ARN="test-secret-arn",
    )

    with pytest.raises(
        ValueError,
        match="must contain username and password fields",
    ):
        _ = settings.database_credentials



def test_missing_all_credentials_raises_value_error(base_settings):
    """Reject configurations with neither AWS nor local credentials."""

    with patch.dict(
        "os.environ",
        {
            "POSTGRES_USER": "",
            "POSTGRES_PASSWORD": "",
            "AWS_SECRET_ARN": "",
        },
    ):
        settings = Settings(
            **base_settings,
            _env_file=None,
            POSTGRES_USER=None,
            POSTGRES_PASSWORD=None,
            AWS_SECRET_ARN=None,
        )

    with pytest.raises(
        ValueError,
        match="Configure AWS_SECRET_ARN",
    ):
        _ = settings.database_credentials




def test_database_url_uses_environment_credentials(base_settings):
    """Build a PostgreSQL URL using local credentials."""
    settings = Settings(
        **base_settings,
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
    )

    assert settings.DATABASE_URL == (
        "postgresql://test_user:test_password@localhost:5432/shortnd_test"
    )


def test_database_url_uses_secrets_manager_credentials(base_settings):
    """Build a PostgreSQL URL using credentials retrieved from AWS."""
    with patch("app.config.boto3.client") as mock_boto_client:
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "SecretString": json.dumps(
                {
                    "username": "shortnd_admin",
                    "password": "test_secret_password",
                }
            )
        }

        settings = Settings(
            **base_settings,
            AWS_SECRET_ARN="test-secret-arn",
        )

        assert settings.DATABASE_URL == (
            "postgresql://shortnd_admin:test_secret_password@"
            "localhost:5432/shortnd_test"
        )

