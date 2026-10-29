
import asyncio
from unittest.mock import patch

from app.main import startup_event, shutdown_event


def test_startup_event_logs_message():
    """Verify that application startup logs the expected message."""
    with patch("app.main.logger.info") as mock_logger:
        asyncio.run(startup_event())

    mock_logger.assert_called_once_with(
        "Starting up the application..."
    )


def test_shutdown_event_logs_message():
    """Verify that application shutdown logs the expected message."""
    with patch("app.main.logger.info") as mock_logger:
        asyncio.run(shutdown_event())

    mock_logger.assert_called_once_with(
        "Shutting down the application..."
    )

