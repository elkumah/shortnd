from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


def test_startup_event_logs_message():
    with patch("app.main.logger.info") as mock_logger, TestClient(app):
        mock_logger.assert_any_call(
            "Starting up the application..."
        )


def test_shutdown_event_logs_message():
    with patch("app.main.logger.info") as mock_logger:
        with TestClient(app):
            pass

        mock_logger.assert_any_call(
            "Shutting down the application..."
        )