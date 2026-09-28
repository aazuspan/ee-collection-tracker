import json
from pathlib import Path

import pytest
from conftest import REPO_ROOT

from ee_collection_tracker.datasets import HLSL, HLSS, Landsat, Sentinel2
from ee_collection_tracker.datasets._dataset import SCHEMA_PATH


@pytest.fixture
def written_schema(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Write the schema for all datasets into an empty directory and return it."""
    monkeypatch.chdir(tmp_path)
    SCHEMA_PATH.parent.mkdir(parents=True)
    for dataset in (Landsat(), Sentinel2(), HLSS(), HLSL()):
        dataset.write_schema()
    return json.loads(SCHEMA_PATH.read_text())


def test_hls_shares_entry(written_schema: dict):
    assert written_schema["hls"]["collections"] == [*HLSS.collection_ids, *HLSL.collection_ids]


def test_committed_schema_is_current(written_schema: dict):
    """The committed schema should match the datasets, e.g. after renaming a label."""
    assert written_schema == json.loads((REPO_ROOT / SCHEMA_PATH).read_text())


def test_schema_paths_exist():
    schema_dir = REPO_ROOT / SCHEMA_PATH.parent
    schema = json.loads((schema_dir / SCHEMA_PATH.name).read_text())

    for entry in schema.values():
        assert (schema_dir / entry["data"]).is_file()
        assert (schema_dir / entry["grid"]).is_file()
