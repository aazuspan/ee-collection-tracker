import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Self

import ee
import geopandas as gpd
import numpy as np
import pandas as pd
from loguru import logger

from ee_collection_tracker.utils import datetime_column_to_epoch_seconds

TIME_START_COL = "TIME_START"
NODATA = 0
_UPDATE_HEADER = "# updated:"
DAY = 86_400

SCHEMA_PATH = Path("site/data/datasets.json")
"""Path to the schema shared by all datasets, describing how the frontend should load them."""


@dataclass
class CollectionSummary:
    collection_id: str
    last_acquisition: datetime
    last_update: datetime

    def minimum_latency(self):
        return self.last_update - self.last_acquisition


@dataclass
class DatasetDiff:
    added: int
    updated: int
    largest_update_days: float
    smallest_update_days: float
    newest_added: datetime | None
    oldest_added: datetime | None

    @classmethod
    def from_states(cls, t1: pd.Series, t2: pd.Series) -> Self:
        """Compute a diff between old and new timestamps."""
        # Timestamps that became valid are additions
        added = (t1 == NODATA) & (t2 != NODATA)
        num_added = added.sum()
        if num_added == 0:
            oldest_added = None
            newest_added = None
        else:
            oldest_added = datetime.fromtimestamp(t2[added].min(), UTC)
            newest_added = datetime.fromtimestamp(t2[added].max(), UTC)

        # Timestamps that changed are updates
        updated = (t1 != NODATA) & (t2 != NODATA) & (t2 != t1)
        num_updated = updated.sum()
        if num_updated == 0:
            smallest_update_days = 0.0
            biggest_update_days = 0.0
        else:
            updated_delta = t2[updated] - t1[updated]
            smallest_update_days = updated_delta.min() / DAY
            biggest_update_days = updated_delta.max() / DAY

        return cls(
            added=num_added,
            updated=num_updated,
            smallest_update_days=smallest_update_days,
            largest_update_days=biggest_update_days,
            oldest_added=oldest_added,
            newest_added=newest_added,
        )


class Dataset(ABC):
    """A dataset that can be queried for timestamps.

    A dataset represents one or more Earth Engine image collection that can be queried with the same
    strategy.
    """

    data_path: Path
    """Path to the initialized data, i.e. asset timestamps organized by index columns."""

    collection_ids: tuple[str]
    """IDs of image collections that are independently tracked within the dataset."""

    derived_collection_ids: dict[str, str]
    """Mapping from base collection IDs to their derived counterparts, if any."""

    index_dtypes: dict[str, str]
    """Column names and dtypes that identify the tracked unit, e.g. a grid cell."""

    label: str
    """Human-readable name of the dataset."""

    grid_path: Path
    """Path to the GeoJSON grid with geometries keyed by the index columns."""

    feature_label: str
    """Template for labeling a grid cell, with index columns in braces, e.g. `Path {PATH}`."""

    schema_path: Path = SCHEMA_PATH
    """Path to the schema shared by all datasets, describing how the frontend should load them."""

    @property
    def index_columns(self) -> tuple[str, ...]:
        return tuple(self.index_dtypes)

    def update(self):
        """Update the dataset state, or initialize if needed.

        Results are written to `data_path`.
        """
        is_initial_run = not self.is_initialized()
        verb = "Initializing" if is_initial_run else "Updating"
        logger.info(f"{verb} {self.label}")
        try:
            # Try loading the data, even if it's not initialized. If two datasets share the same
            # data file, the one that's initialized second should append into the file rather
            # than overwriting it.
            data = self.load_data()
        except Exception:
            logger.debug("Creating empty dataset")
            data = pd.DataFrame(columns=self.index_columns)

        for i, collection_id in enumerate(self.collection_ids):
            logger.info(f"Collection {i + 1} of {len(self.collection_ids)}: {collection_id}")

            collection = self._get_collection(collection_id)
            data = self._update_collection(
                collection=collection,
                collection_id=collection_id,
                old_state=data,
            )

        self.save(data)
        self.write_schema()

    def _get_collection(self, collection_id: str) -> ee.ImageCollection:
        """Build the Earth Engine collection to query."""
        collection = ee.ImageCollection(collection_id)
        # For an update, just focus on the current and previous year to reduce computation time.
        if self.is_initialized():
            now = datetime.now(UTC)
            collection = collection.filterDate(ee.Date(now).advance(-1, "year"), ee.Date(now))
        return collection

    def is_initialized(self) -> bool:
        try:
            # Read just the file header to ensure that collection columns are present. If any are
            # missing, the file isn't fully initialized. This allows multiple datasets to share the
            # same data file, since each checks for its own collections.
            data = pd.read_csv(self.data_path, comment="#", nrows=0)
            return set(self.collection_ids).issubset(data.columns)
        # If the file doesn't exist or is unreadable, consider it uninitialized
        except Exception:
            return False

    def load_data(self) -> gpd.GeoDataFrame:
        """Load the pre-initialized data grid.

        Sub-classes can override to implement additional pre-processing.
        """
        return pd.read_csv(self.data_path, comment="#")

    def read_last_data_update(self) -> datetime:
        """Read the update timestamp from the data path.

        The update timestamp is expected to be in the first line of the file as a comment in the
        format `# updated: <timestamp>`.
        """
        with open(self.data_path) as f:
            first_line = f.readline().strip()
            if not first_line.startswith(_UPDATE_HEADER):
                raise ValueError(f"No `{_UPDATE_HEADER}` timestamp found in {self.data_path}")
        timestamp = int(first_line[len(_UPDATE_HEADER) :].strip())
        return datetime.fromtimestamp(timestamp, UTC)

    @abstractmethod
    def _chunks(self) -> list[tuple[int, int]]:
        """Split the query into inclusive (start, end) chunks passed to `_query_chunk`."""

    @abstractmethod
    def _query_chunk(self, collection: ee.ImageCollection, start: int, end: int) -> pd.DataFrame:
        """Execute an Earth Engine query for one chunk of the given collection.

        Return a dataframe with the index columns and timestamp column.
        """

    def _query(self, collection: ee.ImageCollection) -> pd.DataFrame:
        """Query each chunk of the collection and combine the results."""
        features = []
        chunks = self._chunks()
        for i, (start, end) in enumerate(chunks):
            logger.debug(f"Querying chunk {i + 1} of {len(chunks)}: {start} to {end}")
            chunk_features = self._query_chunk(collection, start, end)
            logger.debug(f"Retrieved {len(chunk_features)} features for chunk")
            features.append(chunk_features)

        return self._combine_chunks(features)

    def _combine_chunks(self, features: list[pd.DataFrame]) -> pd.DataFrame:
        """Combine chunked query results, keeping the latest timestamp per index."""
        return (
            pd.concat(features)
            # Chunks may overlap in index, e.g. across time periods -- keep the latest
            .sort_values(TIME_START_COL)
            .drop_duplicates(list(self.index_columns), keep="last")
            .astype({TIME_START_COL: "datetime64[ms, UTC]", **self.index_dtypes})
        )

    def save(self, data: gpd.GeoDataFrame):
        """Write the GeoDataframe to `data_path` with a timestamp property."""
        updated = int(datetime.now(UTC).timestamp())

        # Drop rows with no timestamp in any collection to save storage. This includes columns
        # written by other datasets that share the data file.
        collection_columns = [c for c in data.columns if c not in self.index_columns]
        nan_rows = data[data[collection_columns].isna().all(axis=1)]
        sorted_columns = list(self.index_columns) + sorted(collection_columns)
        data = (
            data.drop(nan_rows.index)
            # Fill missing timestamps with the no-data value and cast to integer seconds
            .fillna({c: NODATA for c in collection_columns})
            .astype({c: int for c in collection_columns})
            # Sort by the index columns to maintain a consistent order
            .sort_values(list(self.index_columns))
            # Ensure columns are in sorted order
            .loc[:, sorted_columns]
        )

        with open(self.data_path, "w") as f:
            # Write a header comment with the update timestamp
            f.write(f"{_UPDATE_HEADER} {updated}\n")
            data.to_csv(f, index=False)

    def write_schema(self):
        """Describe the dataset in the schema shared by all datasets.

        Entries are keyed by the data file name. Datasets that share a data file share an entry,
        with each adding its collections.
        """
        try:
            schema = json.loads(self.schema_path.read_text())
            logger.debug(f"Loaded schema from {self.schema_path}")
        except FileNotFoundError:
            schema = {}
            logger.debug(f"Initializing new schema at {self.schema_path}")

        def relative_path(path: Path) -> str:
            return (
                path.resolve()
                .relative_to(self.schema_path.resolve().parent, walk_up=True)
                .as_posix()
            )

        key = self.data_path.stem
        collections = schema.get(key, {}).get("collections", [])
        collections += [c for c in self.collection_ids if c not in collections]
        schema[key] = {
            "label": self.label,
            "data": relative_path(self.data_path),
            "grid": relative_path(self.grid_path),
            "index": list(self.index_columns),
            "featureLabel": self.feature_label,
            "collections": collections,
        }

        self.schema_path.write_text(json.dumps(schema, indent=2) + "\n")

    def _update_collection(
        self,
        *,
        collection: ee.ImageCollection,
        collection_id: str,
        old_state: gpd.GeoDataFrame,
    ) -> gpd.GeoDataFrame:
        """Query the given collection and insert timestamps into the old_state.

        Timestamps are in integer epoch seconds using the `collection_id` as the key.
        """
        new_state = self._query(collection).rename(columns={TIME_START_COL: collection_id})
        logger.info(f"Retrieved {len(new_state)} assets")

        # Serialize the datetime to epoch seconds and round to integer. We'll need to
        # round again after merging and filling NaNs, but do it here first so we can
        # compare accurately with the previous rounded state.
        new_state[collection_id] = datetime_column_to_epoch_seconds(new_state[collection_id])

        # On an initial run, the old state won't contain the collection ID column. Populate it so we
        # get a consistent merge output.
        if collection_id not in old_state.columns:
            old_state = old_state.assign(**{collection_id: NODATA})

        # Merge the old and new states. Other collections are kept as-is, while the active
        # collection is split into an old and new column that we can diff and resolve.
        old_col, new_col = f"{collection_id}_old", f"{collection_id}_new"
        outer_state = old_state.merge(
            new_state,
            on=self.index_columns,
            how="outer",
            suffixes=("_old", "_new"),
        ).fillna({old_col: NODATA, new_col: NODATA})

        # Record any changes between the old and new states
        diff = DatasetDiff.from_states(
            t1=outer_state[f"{collection_id}_old"],
            t2=outer_state[f"{collection_id}_new"],
        )
        if diff.updated != 0:
            logger.info(
                f"Updated {diff.updated} assets "
                f"({diff.smallest_update_days:.0f} - {diff.largest_update_days:.0f} days)"
            )
        if diff.added != 0:
            logger.info(
                f"Added {diff.added} assets "
                f"({diff.oldest_added:%Y-%m-%d %H:%M:%S} - {diff.newest_added:%Y-%m-%d %H:%M:%S})"
            )

        if diff.updated == 0 and diff.added == 0:
            logger.info("No changes")

        # Carry old timestamps forward if the new timestamp is null to prevent dropping records.
        # Since updates run on a subset of the full collection, it's possible that an infrequently
        # acquired cell is captured on the initial run and missed on a subsequent update.
        outer_state[collection_id] = np.where(
            outer_state[new_col].eq(NODATA), outer_state[old_col], outer_state[new_col]
        )
        return outer_state.drop(columns=[old_col, new_col])

    def summarize(self) -> list[CollectionSummary]:
        """Return a summary of each collection."""
        if not self.is_initialized():
            return []

        grid = self.load_data()
        last_update = self.read_last_data_update()
        collection_columns = [col for col in grid.columns if col in self.collection_ids]

        summaries: list[CollectionSummary] = []
        for col in collection_columns:
            last_acquisition = datetime.fromtimestamp(grid[col].max(), UTC)
            summaries.append(
                CollectionSummary(
                    collection_id=col, last_acquisition=last_acquisition, last_update=last_update
                )
            )

        return summaries
