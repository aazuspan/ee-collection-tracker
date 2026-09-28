import json
from unittest.mock import MagicMock

import pandas as pd
import pytest
from conftest import REPO_ROOT

from ee_collection_tracker.datasets import _dataset, landsat
from ee_collection_tracker.datasets._dataset import TIME_START_COL
from ee_collection_tracker.datasets.landsat import Landsat


def _chunk_features(paths: list[int], rows: list[int], times_ms: list[int]) -> pd.DataFrame:
    """Build a fake `computeFeatures` result."""
    return pd.DataFrame(
        {"geo": [None] * len(paths), TIME_START_COL: times_ms, "PATH": paths, "ROW": rows}
    )


def test_chunks_cover_all_paths():
    chunks = Landsat()._chunks()

    assert chunks[0] == (1, 10)
    assert chunks[-1] == (231, 233)
    paths = [p for start, end in chunks for p in range(start, end + 1)]
    assert paths == list(range(1, 234))


@pytest.mark.parametrize("chunk_size", [1, 7, 233, 500])
def test_chunks_sizes(chunk_size: int):
    chunks = Landsat()._chunks(chunk_size)

    assert all(end - start + 1 <= chunk_size for start, end in chunks)
    assert sum(end - start + 1 for start, end in chunks) == 233


def test_query_chunk(monkeypatch: pytest.MonkeyPatch):
    ee = MagicMock()
    ee.data.computeFeatures.return_value = _chunk_features([11], [1], [1_700_000_000_000])
    monkeypatch.setattr(landsat, "ee", ee)

    result = Landsat()._query_chunk(MagicMock(), 11, 20)

    ee.Filter.rangeContains.assert_called_once_with("WRS_PATH", 11, 20)
    assert ee.data.computeFeatures.call_args.args[0]["fileFormat"] == "PANDAS_DATAFRAME"
    assert list(result.columns) == [TIME_START_COL, "PATH", "ROW"]


def test_get_collection(monkeypatch: pytest.MonkeyPatch, tmp_path):
    ee = MagicMock()
    monkeypatch.setattr(landsat, "ee", ee)
    monkeypatch.setattr(_dataset, "ee", ee)
    dataset = Landsat()
    dataset.data_path = tmp_path / "landsat.csv"

    result = dataset._get_collection("LANDSAT/LC09/C02/T1")

    # Night-time rows are excluded
    ee.Filter.lt.assert_called_once_with("WRS_ROW", 123)
    ee.ImageCollection.assert_called_once_with("LANDSAT/LC09/C02/T1")
    collection = ee.ImageCollection.return_value
    # The full collection is queried on initialization
    collection.filterDate.assert_not_called()
    assert result == collection.filter.return_value


def test_combine_chunks():
    features = [
        _chunk_features([1, 2], [10, 20], [1_700_000_000_123, 1_700_000_001_000]),
        _chunk_features([11], [122], [1_700_000_002_000]),
    ]
    features = [f.drop(columns=["geo"]) for f in features]

    result = Landsat()._combine_chunks(features)

    assert len(result) == 3
    assert result["PATH"].dtype == "uint8"
    assert result["ROW"].dtype == "uint8"
    assert str(result[TIME_START_COL].dtype) == "datetime64[ms, UTC]"
    assert result[TIME_START_COL].min() == pd.Timestamp(1_700_000_000_123, unit="ms", tz="UTC")


def test_update_landsat(monkeypatch: pytest.MonkeyPatch):
    init = MagicMock()
    update = MagicMock()
    monkeypatch.setattr(landsat, "initialize_service_account", init)
    monkeypatch.setattr(Landsat, "update", update)

    landsat.update_landsat()

    init.assert_called_once()
    update.assert_called_once()


def test_grid():
    features = json.loads((REPO_ROOT / Landsat.grid_path).read_text())["features"]
    grid = pd.DataFrame([f["properties"] for f in features])

    assert list(grid.columns) == list(Landsat.index_dtypes)
    assert not grid.duplicated().any()
    assert grid["PATH"].between(1, 233).all()
    # Night-time rows are excluded
    assert grid["ROW"].between(1, 122).all()
