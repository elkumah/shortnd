from app.logging.logger import load_logging_config


def test_load_logging_config_uses_fallback_when_file_missing(
    tmp_path,
    caplog,
):
    missing_config = tmp_path / "missing_logging_config.json"

    load_logging_config(str(missing_config))

    assert "not found" in caplog.text


def test_load_logging_config_uses_fallback_for_invalid_json(tmp_path):
    invalid_config = tmp_path / "invalid_logging_config.json"

    invalid_config.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    load_logging_config(str(invalid_config))