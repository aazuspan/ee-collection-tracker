import json
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from ee_collection_tracker import utils


def test_datetime_column_to_epoch_seconds():
    col = pd.Series(
        pd.to_datetime(
            ["1970-01-01T00:00:00", "2026-01-01T00:00:01.999"], utc=True, format="ISO8601"
        )
    ).astype("datetime64[ms, UTC]")

    result = utils.datetime_column_to_epoch_seconds(col)

    # Fractional seconds are truncated
    assert result.tolist() == [0, 1767225601]
    assert result.dtype == int


@pytest.fixture
def ee(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    monkeypatch.setattr(utils, "ee", mock)
    monkeypatch.delenv("EE_SERVICE_ACCOUNT", raising=False)
    monkeypatch.delenv("EE_SERVICE_ACCOUNT_PATH", raising=False)
    return mock


def test_initialize_from_env(ee: MagicMock, monkeypatch: pytest.MonkeyPatch):
    key_data = json.dumps({"project_id": "my-project"})
    monkeypatch.setenv("EE_SERVICE_ACCOUNT", key_data)

    utils.initialize_service_account()

    ee.ServiceAccountCredentials.assert_called_once_with(key_data=key_data)
    ee.Initialize.assert_called_once_with(
        ee.ServiceAccountCredentials.return_value, project="my-project"
    )


def test_initialize_from_file(ee: MagicMock, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    key_file = tmp_path / "key.json"
    key_file.write_text("{}")
    monkeypatch.setenv("EE_SERVICE_ACCOUNT_PATH", str(key_file))

    utils.initialize_service_account()

    ee.ServiceAccountCredentials.assert_called_once_with(key_file=key_file.as_posix())
    ee.Initialize.assert_called_once_with(ee.ServiceAccountCredentials.return_value)


def test_initialize_persistent(ee: MagicMock, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("EE_SERVICE_ACCOUNT_PATH", str(tmp_path / "missing.json"))

    utils.initialize_service_account()

    ee.ServiceAccountCredentials.assert_not_called()
    ee.Initialize.assert_called_once_with("persistent")
