from datetime import UTC, datetime
from pathlib import Path

import pytest
import snakemd

from ee_collection_tracker import readme
from ee_collection_tracker.datasets._dataset import CollectionSummary

SUMMARIES = [
    CollectionSummary(
        collection_id="LANDSAT/LC09/C02/T1",
        last_acquisition=datetime(2026, 9, 27, 7, 29, 1, tzinfo=UTC),
        last_update=datetime(2026, 9, 30, 19, 47, 25, tzinfo=UTC),
    ),
    CollectionSummary(
        collection_id="COPERNICUS/S2",
        last_acquisition=datetime(2026, 9, 30, 15, 32, 51, tzinfo=UTC),
        last_update=datetime(2026, 9, 30, 19, 55, 59, tzinfo=UTC),
    ),
]


@pytest.fixture
def workflow_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Point the README generator at a temporary update workflow."""
    path = tmp_path / "update.yaml"
    monkeypatch.setattr(readme, "_UPDATE_WORKFLOW", path)
    return path


def write_workflow(path: Path, cron: str) -> None:
    path.write_text(
        f"""
name: Update data
on:
  workflow_dispatch:
  schedule:
  - cron: '{cron}'
"""
    )


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("30 23 * * *", ("23:30",)),
        ("0 6,18 * * *", ("06:00", "18:00")),
        ("0,30 6,18 * * *", ("06:00", "06:30", "18:00", "18:30")),
    ],
)
def test_parse_daily_cron(expr: str, expected: tuple[str, ...]):
    assert readme._parse_daily_cron(expr) == expected


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], ""),
        (["a"], "a"),
        (["a", "b"], "a and b"),
        (["a", "b", "c"], "a, b and c"),
        (("a", "b"), "a and b"),
    ],
)
def test_join_list(items: list[str], expected: str):
    assert readme._join_list(items) == expected


def test_join_list_conjunction():
    assert readme._join_list(["a", "b"], conjunction="or") == "a or b"


@pytest.mark.parametrize(
    ("cron", "expected"),
    [
        ("30 23 * * *", "daily updates at 23:30 UTC"),
        ("0 6,18 * * *", "daily updates at 06:00 and 18:00 UTC"),
    ],
)
def test_get_workflow_frequency(workflow_path: Path, cron: str, expected: str):
    write_workflow(workflow_path, cron)

    assert readme._get_workflow_frequency() == expected


def test_get_workflow_frequency_missing_workflow(workflow_path: Path):
    assert readme._get_workflow_frequency() == "regular updates"


def test_get_workflow_frequency_unsupported_cron(workflow_path: Path):
    write_workflow(workflow_path, "*/15 * * * *")

    assert readme._get_workflow_frequency() == "regular updates"


def test_get_workflow_frequency_repo_workflow():
    """The real update workflow should be parseable from the repo root."""
    assert readme._get_workflow_frequency().startswith("daily updates at ")


def test_add_intro(workflow_path: Path):
    write_workflow(workflow_path, "30 23 * * *")
    doc = snakemd.new_doc()

    readme.add_intro(doc)

    text = str(doc)
    assert "## Earth Engine collection tracker" in text
    assert "(https://aazuspan.github.io/ee-collection-tracker/)" in text
    assert "with daily updates at 23:30 UTC." in text


def test_add_collection_summary():
    doc = snakemd.new_doc()

    readme.add_collection_summary(doc, SUMMARIES, {"COPERNICUS/S2": "COPERNICUS/S2_HARMONIZED"})

    text = str(doc)
    rows = [line for line in text.splitlines() if line.startswith("| **")]
    cells = [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]
    assert cells == [
        ["**LANDSAT/LC09/C02/T1**", "2026-09-27 07:29:01", "2026-09-30 19:47:25", "3 days"],
        ["**COPERNICUS/S2**", "2026-09-30 15:32:51", "2026-09-30 19:55:59", "4 hours"],
        [
            "**COPERNICUS/S2_HARMONIZED**[^derived]",
            "2026-09-30 15:32:51",
            "2026-09-30 19:55:59",
            "4 hours",
        ],
    ]
    assert "[^derived]: Earth Engine derives this collection" in text


def test_update_readme(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(readme.Landsat, "summarize", lambda self: SUMMARIES[:1])
    monkeypatch.setattr(readme.Sentinel2, "summarize", lambda self: SUMMARIES[1:])

    readme.update_readme()

    text = (tmp_path / "README.md").read_text()
    assert "## Collection summary" in text
    assert "**LANDSAT/LC09/C02/T1**" in text
    assert "**COPERNICUS/S2**" in text
    assert "**COPERNICUS/S2_HARMONIZED**[^derived]" in text
    assert "**LANDSAT/LC09/C02/T1_TOA**[^derived]" in text
