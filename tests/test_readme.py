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


def test_add_intro():
    doc = snakemd.new_doc()

    readme.add_intro(doc, now=datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC))

    text = str(doc)
    assert "## Earth Engine collection tracker" in text
    assert "(https://aazuspan.github.io/ee-collection-tracker/)" in text
    assert "*This README was generated on 2026-01-02 03:04:05.*" in text


def test_add_collection_summary():
    doc = snakemd.new_doc()

    readme.add_collection_summary(doc, SUMMARIES)

    rows = [line for line in str(doc).splitlines() if line.startswith("| **")]
    cells = [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]
    assert cells == [
        ["**LANDSAT/LC09/C02/T1**", "2026-09-27 07:29:01", "2026-09-30 19:47:25", "3 days"],
        ["**COPERNICUS/S2**", "2026-09-30 15:32:51", "2026-09-30 19:55:59", "4 hours"],
    ]


def test_update_readme(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(readme.Landsat, "summarize", lambda self: SUMMARIES[:1])
    monkeypatch.setattr(readme.Sentinel2, "summarize", lambda self: SUMMARIES[1:])

    readme.update_readme()

    text = (tmp_path / "README.md").read_text()
    assert "## Collection summary" in text
    assert "**LANDSAT/LC09/C02/T1**" in text
    assert "**COPERNICUS/S2**" in text
