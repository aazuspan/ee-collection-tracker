from datetime import datetime
from itertools import product
from pathlib import Path

import humanize
import snakemd
import yaml
from loguru import logger

from ee_collection_tracker.datasets import HLSL, HLSS, Landsat, Sentinel2
from ee_collection_tracker.datasets._dataset import CollectionSummary

_UPDATE_WORKFLOW = Path(".github/workflows/update.yaml")


def _format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _parse_daily_cron(expr: str) -> tuple[str, ...]:
    """Parse a daily cron expression into a tuple of 24-hour HH:MM timestamps.

    Only cron expressions with 1 or more explicit hours and minutes are supported.
    """
    minute, hour, _, _, _ = expr.split()
    minutes = map(int, minute.split(","))
    hours = map(int, hour.split(","))
    return tuple(f"{h:02}:{m:02}" for h, m in product(hours, minutes))


def _join_list(items: list[str], conjunction: str = "and") -> str:
    """Join a list of strings with commas and a conjunction before the last item."""
    match items:
        case []:
            return ""
        case [single]:
            return single
        case (*rest, last):
            return ", ".join(rest) + f" {conjunction} " + last


def _get_workflow_frequency() -> str:
    """Describe the cron frequency from the update workflow.

    This is best-effort and falls back to vague "regular updates" rather than crashing.
    """
    try:
        with open(_UPDATE_WORKFLOW) as f:
            workflow = yaml.safe_load(f)

        # 'on' gets parsed to boolean True in YAML
        on = True
        expr = workflow[on]["schedule"][0]["cron"]
        description = _join_list(_parse_daily_cron(expr))

        return f"daily updates at {description} UTC"
    except Exception as e:
        logger.warning("Failed to parse workflow frequency: {}", e)
        return "regular updates"


def update_readme() -> None:
    active_datasets = [Landsat(), Sentinel2(), HLSS(), HLSL()]
    collection_summaries = [c for dataset in active_datasets for c in dataset.summarize()]
    derived_collections = {
        source: target
        for dataset in active_datasets
        for source, target in dataset.derived_collection_ids.items()
    }
    doc = snakemd.new_doc()
    add_intro(doc)
    add_collection_summary(doc, collection_summaries, derived_collections)
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


def add_intro(doc: snakemd.Document) -> None:
    doc.add_heading("Earth Engine collection tracker", level=2)
    add_badges(doc)
    interactive_map_link = snakemd.Inline(
        "interactive map", link="https://aazuspan.github.io/ee-collection-tracker/"
    )

    update_frequency = _get_workflow_frequency()
    doc.add_paragraph(
        "This repository tracks the the availability of selected Earth Engine "
        f"collections with {update_frequency}. Explore the latest acquisition on the "
        f"{interactive_map_link}."
    )


def add_collection_summary(
    doc: snakemd.Document,
    collection_summaries: list[CollectionSummary],
    derived_collections: dict[str, str],
) -> None:
    doc.add_heading("Collection summary", level=2)

    doc.add_paragraph(
        "The table below shows the most recent acquisition `system:time_start` for "
        "each tracked collection, along with the time that assets were last queried "
        "and updated, and the age of the newest asset during the last query. All times "
        "are in UTC."
    )

    header = ["Collection ID", "Last acquisition", "Last update", "Newest asset"]

    rows = []
    for c in collection_summaries:
        rows.append(
            [
                f"**{c.collection_id}**",
                _format_datetime(c.last_acquisition),
                _format_datetime(c.last_update),
                humanize.naturaldelta(c.minimum_latency()),
            ]
        )
        if c.collection_id in derived_collections:
            rows.append(
                [
                    f"**{derived_collections[c.collection_id]}**[^derived]",
                    _format_datetime(c.last_acquisition),
                    _format_datetime(c.last_update),
                    humanize.naturaldelta(c.minimum_latency()),
                ]
            )

    doc.add_table(header=header, data=rows)
    doc.add_paragraph(
        "[^derived]: Earth Engine derives this collection by processing another collection "
        "on-the-fly. For efficiency, only the source collection is tracked."
    )
