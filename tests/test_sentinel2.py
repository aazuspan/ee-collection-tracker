import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest
from conftest import REPO_ROOT

from ee_collection_tracker.datasets import _dataset, _mgrs, sentinel2
from ee_collection_tracker.datasets._dataset import TIME_START_COL
from ee_collection_tracker.datasets.sentinel2 import Sentinel2


@pytest.fixture
def dataset(tmp_path: Path) -> Sentinel2:
    dataset = Sentinel2()
    dataset.data_path = tmp_path / "sentinel2.csv"
    return dataset


def _mock_query_result(collection: MagicMock, groups: list[dict]) -> None:
    reduced = collection.filter.return_value.reduceColumns.return_value
    reduced.getInfo.return_value = {"groups": groups}


def test_chunks_update(dataset: Sentinel2):
    dataset.save(
        pd.DataFrame({"MGRS_TILE": ["10TEK"], "COPERNICUS/S2": [1], "COPERNICUS/S2_SR": [1]})
    )
    year = datetime.now(UTC).year

    assert dataset._chunks() == [(year - 1, year - 1), (year, year)]


def test_chunks_initial(dataset: Sentinel2):
    year = datetime.now(UTC).year

    assert dataset._chunks() == [(y, y) for y in range(2015, year + 1)]


def test_chunks_multi_year(dataset: Sentinel2):
    year = datetime.now(UTC).year
    chunks = dataset._chunks(chunk_size=5)

    assert chunks[0] == (2015, 2019)
    assert chunks[-1][1] == year
    assert [y for start, end in chunks for y in range(start, end + 1)] == list(
        range(2015, year + 1)
    )


def test_query_chunk(monkeypatch: pytest.MonkeyPatch, dataset: Sentinel2):
    ee = MagicMock()
    monkeypatch.setattr(_mgrs, "ee", ee)
    collection = MagicMock()
    _mock_query_result(collection, [{"MGRS_TILE": "10TEK", "max": 123}])

    result = dataset._query_chunk(collection, 2020, 2021)

    ee.Filter.calendarRange.assert_called_once_with(2020, 2021, "year")
    assert result.to_dict("records") == [{TIME_START_COL: 123, "MGRS_TILE": "10TEK"}]


def test_query_chunk_empty(monkeypatch: pytest.MonkeyPatch, dataset: Sentinel2):
    monkeypatch.setattr(_mgrs, "ee", MagicMock())
    collection = MagicMock()
    _mock_query_result(collection, [])

    result = dataset._query_chunk(collection, 2020, 2020)

    assert result.empty
    assert set(result.columns) == {TIME_START_COL, "MGRS_TILE"}


def test_get_collection(monkeypatch: pytest.MonkeyPatch, dataset: Sentinel2):
    ee = MagicMock()
    monkeypatch.setattr(sentinel2, "ee", ee)
    monkeypatch.setattr(_dataset, "ee", ee)

    result = dataset._get_collection("COPERNICUS/S2")

    # Ascending night-time passes are excluded
    ee.Filter.eq.assert_called_once_with("SENSING_ORBIT_DIRECTION", "DESCENDING")
    ee.ImageCollection.assert_called_once_with("COPERNICUS/S2")
    assert result == ee.ImageCollection.return_value.filter.return_value


def test_combine_chunks_keeps_latest(dataset: Sentinel2):
    features = [
        pd.DataFrame({TIME_START_COL: [100, 300], "MGRS_TILE": ["10TEK", "11SKA"]}),
        pd.DataFrame({TIME_START_COL: [200, 250], "MGRS_TILE": ["10TEK", "11SKA"]}),
        pd.DataFrame({TIME_START_COL: [], "MGRS_TILE": []}),
    ]

    result = dataset._combine_chunks(features).set_index("MGRS_TILE")[TIME_START_COL]

    assert result.to_dict() == {
        "10TEK": pd.Timestamp(200, unit="ms", tz="UTC"),
        "11SKA": pd.Timestamp(300, unit="ms", tz="UTC"),
    }
    assert str(result.dtype) == "datetime64[ms, UTC]"


def test_grid():
    features = json.loads((REPO_ROOT / Sentinel2.grid_path).read_text())["features"]
    tiles = pd.Series([f["properties"]["MGRS_TILE"] for f in features])

    assert tiles.str.fullmatch(r"\d{2}[A-Z]{3}").all()
