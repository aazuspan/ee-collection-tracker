from pathlib import Path

import pandas as pd
import pytest

from ee_collection_tracker.datasets._dataset import TIME_START_COL, Dataset

REPO_ROOT = Path(__file__).parents[1]


def to_datetimes(seconds: list[int]) -> pd.Series:
    """Convert epoch seconds to a UTC datetime series, as returned by a dataset query."""
    return pd.to_datetime(pd.Series(seconds), unit="s", utc=True).astype("datetime64[ms, UTC]")


def query_result(ids: list[int], seconds: list[int]) -> pd.DataFrame:
    """Build a fake query result for `FakeDataset`."""
    return pd.DataFrame({"ID": ids, TIME_START_COL: to_datetimes(seconds)})


class FakeDataset(Dataset):
    """A dataset that returns canned query results instead of querying Earth Engine."""

    label = "Fake"
    collection_ids = ("A", "B")
    index_dtypes = {"ID": "int64"}
    feature_label = "Cell {ID}"

    def __init__(self, tmp_path: Path, results: dict[str, pd.DataFrame]):
        self.data_path = tmp_path / "fake.csv"
        self.grid_path = tmp_path / "grid" / "fake.geojson"
        self.schema_path = tmp_path / "datasets.json"
        self.results = results
        self.collection_calls: list[tuple[str, bool]] = []

    def _get_collection(self, collection_id: str) -> str:
        self.collection_calls.append((collection_id, not self.is_initialized()))
        # The "collection" is just the ID, which `_query_chunk` uses to look up results.
        return collection_id

    def _chunks(self) -> list[tuple[int, int]]:
        return [(0, 0)]

    def _query_chunk(self, collection: str, start: int, end: int) -> pd.DataFrame:
        return self.results[collection].copy()


@pytest.fixture
def fake_dataset(tmp_path: Path) -> FakeDataset:
    return FakeDataset(
        tmp_path,
        results={
            "A": query_result([1, 2, 3], [100, 200, 300]),
            "B": query_result([2, 4], [400, 500]),
        },
    )
