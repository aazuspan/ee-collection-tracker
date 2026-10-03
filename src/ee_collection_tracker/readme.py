from datetime import UTC, datetime

import humanize
import snakemd

from ee_collection_tracker.datasets import HLSL, HLSS, Landsat, Sentinel2
from ee_collection_tracker.datasets._dataset import CollectionSummary


def _format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def update_readme() -> None:
    active_datasets = [Landsat(), Sentinel2(), HLSS(), HLSL()]
    doc = snakemd.new_doc()
    add_intro(doc, now=datetime.now(UTC))
    add_collection_summary(doc, [c for dataset in active_datasets for c in dataset.summarize()])
    doc.dump("README")


def add_badges(doc: snakemd.Document) -> None:
    workflows = {"Update": "update.yaml", "Deploy": "pages.yaml", "Test": "test.yaml"}

    workflow_root = "https://github.com/aazuspan/ee-collection-tracker/actions/workflows"
    badges = [
        snakemd.Inline(
            text=name, image=f"{workflow_root}/{file}/badge.svg", link=f"{workflow_root}/{file}"
        )
        for name, file in workflows.items()
    ]

    doc.add_paragraph(" ".join(f"{badge}" for badge in badges))


def add_intro(doc: snakemd.Document, now: datetime) -> None:
    doc.add_heading("Earth Engine collection tracker", level=2)
    add_badges(doc)
    interactive_map_link = snakemd.Inline(
        "interactive map", link="https://aazuspan.github.io/ee-collection-tracker/"
    )

    doc.add_paragraph(
        "This repository tracks the the availability of selected Earth Engine "
        "collections with daily updates. Explore the latest acquisition on the "
        f"{interactive_map_link}."
    )

    doc.add_paragraph(f"*This README was generated on {_format_datetime(now)}.*")


def add_collection_summary(
    doc: snakemd.Document, collection_summaries: list[CollectionSummary]
) -> None:
    doc.add_heading("Collection summary", level=2)

    doc.add_paragraph(
        "The table below shows the most recent acquisition `system:time_start` for "
        "each tracked collection, along with the time that assets were last queried "
        "and updated, and the age of the newest asset during the last query. All times "
        "are in UTC."
    )

    header = ["Collection ID", "Last acquisition", "Last update", "Newest asset"]
    rows = [
        [
            f"**{c.collection_id}**",
            _format_datetime(c.last_acquisition),
            _format_datetime(c.last_update),
            humanize.naturaldelta(c.minimum_latency()),
        ]
        for c in collection_summaries
    ]

    doc.add_table(header=header, data=rows)

    doc.add_paragraph(
        "Harmonized Sentinel-2 collections are derived from the corresponding "
        "`COPERNICUS` collections above. Landsat TOA products are derived from the "
        "corresponding `C02/T1` collections."
    )
