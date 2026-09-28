import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest
from conftest import FakeDataset, query_result

from ee_collection_tracker.datasets._dataset import TIME_START_COL, CollectionSummary

DAY = 86400


def test_minimum_latency():
    summary = CollectionSummary(
        collection_id="A",
        last_acquisition=datetime(2026, 1, 1, tzinfo=UTC),
        last_update=datetime(2026, 1, 3, 12, tzinfo=UTC),
    )
    assert summary.minimum_latency() == timedelta(days=2, hours=12)


def test_get_diff(fake_dataset: FakeDataset):
    old = pd.DataFrame({"ID": [1, 2, 3, 4], "A": [0, 100, DAY, DAY]})
    new = pd.DataFrame({"ID": [1, 2, 3, 5], "A": [DAY, 100, 3 * DAY, DAY]})

    diff = fake_dataset._get_diff(old, new, time_col="A")

    # 1 and 5 were added, 3 was updated, 4 was removed, 2 is unchanged
    assert diff.added == 2
    assert diff.updated == 1
    assert diff.removed == 1
    assert diff.min_update_days == pytest.approx(2)
    assert diff.max_update_days == pytest.approx(2)


def test_get_diff_update_range(fake_dataset: FakeDataset):
    old = pd.DataFrame({"ID": [1, 2], "A": [DAY, DAY]})
    new = pd.DataFrame({"ID": [1, 2], "A": [2 * DAY, 5 * DAY]})

    diff = fake_dataset._get_diff(old, new, time_col="A")

    assert diff.updated == 2
    assert diff.min_update_days == pytest.approx(1)
    assert diff.max_update_days == pytest.approx(4)


def test_get_diff_no_changes(fake_dataset: FakeDataset):
    state = pd.DataFrame({"ID": [1, 2], "A": [DAY, 0]})

    diff = fake_dataset._get_diff(state, state.copy(), time_col="A")

    assert (diff.added, diff.removed, diff.updated) == (0, 0, 0)
    assert diff.min_update_days == 0
    assert diff.max_update_days == 0


def test_get_diff_missing_old_column(fake_dataset: FakeDataset):
    """On an initial run the grid has no column for the collection yet."""
    old = pd.DataFrame({"ID": [1, 2]})
    new = pd.DataFrame({"ID": [1], "A": [DAY]})

    diff = fake_dataset._get_diff(old, new, time_col="A")

    assert (diff.added, diff.removed, diff.updated) == (1, 0, 0)


def read_data(dataset: FakeDataset) -> pd.DataFrame:
    return pd.read_csv(dataset.data_path, comment="#")


def test_update_collection(fake_dataset: FakeDataset):
    grid = pd.DataFrame({"ID": [1, 2, 3], "A": [0, 50, 50], "other": ["x", "y", "z"]})
    fake_dataset.results["A"] = query_result([2, 3, 99], [100, 50, 100])

    result = fake_dataset._update_collection(collection="A", collection_id="A", grid=grid)

    # Existing column is replaced without suffixes, and other columns are kept
    assert list(result.columns) == ["ID", "other", "A"]
    # New rows are added and rows missing from the query are left empty
    assert result["ID"].tolist() == [1, 2, 3, 99]
    assert result["A"].tolist()[1:] == [100, 50, 100]
    assert pd.isna(result["A"].iloc[0])


def test_update_initializes(fake_dataset: FakeDataset):
    assert not fake_dataset.is_initialized()

    before = datetime.now(UTC).replace(microsecond=0)
    fake_dataset.update()

    assert fake_dataset.is_initialized()
    assert fake_dataset.collection_calls == [("A", True), ("B", True)]

    data = read_data(fake_dataset)
    assert list(data.columns) == ["ID", "A", "B"]
    assert data["ID"].tolist() == [1, 2, 3, 4]
    assert data["A"].tolist() == [100, 200, 300, 0]
    assert data["B"].tolist() == [0, 400, 0, 500]

    # The update time is stored in a header comment
    assert before <= fake_dataset.read_last_data_update() <= datetime.now(UTC)


def test_update_uses_existing_data(fake_dataset: FakeDataset):
    fake_dataset.update()
    fake_dataset.collection_calls.clear()
    fake_dataset.results["A"] = query_result([1, 2, 3], [100, 250, 300])

    fake_dataset.update()

    assert fake_dataset.collection_calls == [("A", False), ("B", False)]
    data = read_data(fake_dataset)
    assert data["A"].tolist() == [100, 250, 300, 0]
    assert data["B"].tolist() == [0, 400, 0, 500]


def test_update_writes_schema(fake_dataset: FakeDataset):
    fake_dataset.update()

    schema = json.loads(fake_dataset.schema_path.read_text())

    # Paths are relative to the schema file so the frontend can resolve them
    assert schema == {
        "fake": {
            "label": "Fake",
            "data": "fake.csv",
            "grid": "grid/fake.geojson",
            "index": ["ID"],
            "featureLabel": "Cell {ID}",
            "collections": ["A", "B"],
        }
    }


def test_save_drops_empty_rows(fake_dataset: FakeDataset):
    fake_dataset.save(
        pd.DataFrame({"ID": [3, 1, 2], "A": [100, None, None], "B": [None, None, 200]})
    )

    data = read_data(fake_dataset)

    # Rows are sorted, empty rows are dropped, and missing timestamps are filled with 0
    assert data.to_dict("list") == {"ID": [2, 3], "A": [0, 100], "B": [200, 0]}


class OtherFakeDataset(FakeDataset):
    """A dataset that shares a data file with `FakeDataset`."""

    label = "Other"
    collection_ids = ("C",)


def test_shared_data_file(fake_dataset: FakeDataset, tmp_path: Path):
    other = OtherFakeDataset(tmp_path, results={"C": query_result([4, 5], [600, 700])})
    fake_dataset.update()

    assert not other.is_initialized()
    other.update()

    assert fake_dataset.is_initialized()
    assert other.is_initialized()
    # Existing collections and rows are retained when the second dataset is added
    assert read_data(fake_dataset).to_dict("list") == {
        "ID": [1, 2, 3, 4, 5],
        "A": [100, 200, 300, 0, 0],
        "B": [0, 400, 0, 500, 0],
        "C": [0, 0, 0, 600, 700],
    }
    # Datasets sharing a data file share a schema entry
    schema = json.loads(fake_dataset.schema_path.read_text())
    assert list(schema) == ["fake"]
    assert schema["fake"]["label"] == "Other"
    assert schema["fake"]["collections"] == ["A", "B", "C"]


def test_write_schema_keeps_other_datasets(fake_dataset: FakeDataset):
    fake_dataset.schema_path.write_text(json.dumps({"existing": {"label": "Existing"}}))

    fake_dataset.write_schema()

    schema = json.loads(fake_dataset.schema_path.read_text())
    assert list(schema) == ["existing", "fake"]
    assert schema["existing"] == {"label": "Existing"}


def test_summarize_uninitialized(fake_dataset: FakeDataset):
    assert fake_dataset.summarize() == []


def test_summarize(fake_dataset: FakeDataset):
    fake_dataset.update()
    # The update time comes from the stored timestamp, not the file modification time
    last_update = datetime(2026, 1, 1, tzinfo=UTC)
    _, *lines = fake_dataset.data_path.read_text().splitlines(keepends=True)
    fake_dataset.data_path.write_text(
        f"# updated: {int(last_update.timestamp())}\n" + "".join(lines)
    )
    os.utime(fake_dataset.data_path, (0, 0))

    summaries = fake_dataset.summarize()

    assert summaries == [
        CollectionSummary("A", datetime.fromtimestamp(300, UTC), last_update),
        CollectionSummary("B", datetime.fromtimestamp(500, UTC), last_update),
    ]


def test_summarize_skips_untracked_columns(fake_dataset: FakeDataset):
    fake_dataset.save(pd.DataFrame({"ID": [1], "A": [100], "B": [200], "untracked": [999]}))

    summaries = fake_dataset.summarize()

    assert [s.collection_id for s in summaries] == ["A", "B"]


def test_summarize_missing_timestamp(fake_dataset: FakeDataset):
    pd.DataFrame({"ID": [1], "A": [100], "B": [200]}).to_csv(fake_dataset.data_path, index=False)

    with pytest.raises(ValueError, match="No `# updated:` timestamp"):
        fake_dataset.summarize()


def test_index_columns(fake_dataset: FakeDataset):
    assert fake_dataset.index_columns == ("ID",)


def test_query_combines_chunks(fake_dataset: FakeDataset, monkeypatch: pytest.MonkeyPatch):
    calls = []

    def fake_query_chunk(collection, start, end):
        calls.append((collection, start, end))
        return query_result([1, 2], [start, end])

    monkeypatch.setattr(fake_dataset, "_chunks", lambda: [(10, 20), (30, 5)])
    monkeypatch.setattr(fake_dataset, "_query_chunk", fake_query_chunk)

    result = fake_dataset._query("A")

    assert calls == [("A", 10, 20), ("A", 30, 5)]
    # The latest timestamp per index is kept across chunks
    assert result.set_index("ID")[TIME_START_COL].to_dict() == {
        1: pd.Timestamp(30, unit="s", tz="UTC"),
        2: pd.Timestamp(20, unit="s", tz="UTC"),
    }


def test_combine_chunks_casts_types(fake_dataset: FakeDataset):
    features = [pd.DataFrame({"ID": ["1", "2"], TIME_START_COL: [1_700_000_000_123, 0]})]

    result = fake_dataset._combine_chunks(features)

    assert result["ID"].dtype == "int64"
    assert str(result[TIME_START_COL].dtype) == "datetime64[ms, UTC]"
    assert result[TIME_START_COL].max() == pd.Timestamp(1_700_000_000_123, unit="ms", tz="UTC")
