import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import ee
import geopandas as gpd
import pandas as pd
from loguru import logger

from ee_collection_tracker.utils import datetime_column_to_epoch_seconds

TIME_START_COL = "TIME_START"
_NODATA = 0
_UPDATE_HEADER = "# updated:"

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
    removed: int
    updated: int
    min_update_days: float
    max_update_days: float


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
        try:
            # Try loading the grid, even if it's not initialized. If two datasets share the same
            # data file, the one that's initialized second should append into the file rather
            # than overwriting it.
            data_grid = self.load_data_grid()
        except Exception:
            data_grid = pd.DataFrame(columns=self.index_columns)

        for i, collection_id in enumerate(self.collection_ids):
            logger.info(f"{verb} collection {i + 1} of {len(self.collection_ids)}: {collection_id}")

            collection = self._get_collection(collection_id)
            data_grid = self._update_collection(
                collection=collection,
                collection_id=collection_id,
                grid=data_grid,
            )

        self.save(data_grid)
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

    def load_data_grid(self) -> gpd.GeoDataFrame:
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
        data = (
            data.drop(nan_rows.index)
            # Fill missing timestamps with the no-data value and cast to integer seconds
            .fillna({c: _NODATA for c in collection_columns})
            .astype({c: int for c in collection_columns})
            # Sort by the index columns to maintain a consistent order
            .sort_values(list(self.index_columns))
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
        except FileNotFoundError:
            schema = {}

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
        grid: gpd.GeoDataFrame,
    ) -> gpd.GeoDataFrame:
        """Query the given collection and insert timestamps into the grid.

        Timestamps are in integer epoch seconds using the `collection_id` as the key.
        """
        new_state = self._query(collection).rename(columns={TIME_START_COL: collection_id})
        logger.info(f"Retrieved {len(new_state)} assets")

        # Serialize the datetime to epoch seconds and round to integer. We'll need to
        # round again after merging and filling NaNs, but do it here first so we can
        # compare accurately with the previous rounded state.
        new_state[collection_id] = datetime_column_to_epoch_seconds(new_state[collection_id])

        # Record any changes between the old and new states
        diff = self._get_diff(grid, new_state, time_col=collection_id)
        if diff.updated != 0:
            logger.info(
                f"Updated {diff.updated} assets "
                f"({diff.min_update_days:.0f} - {diff.max_update_days:.0f} days)"
            )
        if diff.added != 0:
            logger.info(f"Added {diff.added} assets")
        if diff.removed != 0:
            logger.info(f"Removed {diff.removed} assets")
        if diff.updated == 0 and diff.added == 0 and diff.removed == 0:
            logger.info("No changes")

        # Drop the old timestamp column to avoid appending a suffix
        return grid.drop(columns=[collection_id], errors="ignore").merge(
            new_state,
            on=self.index_columns,
            # Since we update as we iterate over collections, an outer join ensures we retain
            # existing tiles and add any new ones from the current collection.
            how="outer",
        )

    def _get_diff(
        self, old_state: pd.DataFrame, new_state: pd.DataFrame, time_col: str
    ) -> DatasetDiff:
        # The collection won't be in the old state yet on an initial run
        if time_col not in old_state.columns:
            old_state = old_state.assign(**{time_col: _NODATA})

        merged = old_state.merge(
            new_state,
            on=self.index_columns,
            suffixes=("_old", "_new"),
            how="outer",
        ).fillna({f"{time_col}_old": _NODATA, f"{time_col}_new": _NODATA})

        # Remove unchanged rows
        changed = merged[merged[f"{time_col}_old"] != merged[f"{time_col}_new"]]
        old_time = changed[f"{time_col}_old"]
        new_time = changed[f"{time_col}_new"]

        updated = (old_time != _NODATA) & (new_time > old_time)
        added = (old_time == _NODATA) & (new_time != _NODATA)
        removed = (old_time != _NODATA) & (new_time == _NODATA)
        # Timestamps are already in elapsed seconds
        min_update_days = (new_time[updated] - old_time[updated]).min() / 86400
        max_update_days = (new_time[updated] - old_time[updated]).max() / 86400

        return DatasetDiff(
            added=added.sum(),
            removed=removed.sum(),
            updated=updated.sum(),
            min_update_days=min_update_days if updated.sum() != 0 else 0,
            max_update_days=max_update_days if updated.sum() != 0 else 0,
        )

    def summarize(self) -> list[CollectionSummary]:
        """Return a summary of each collection."""
        if not self.is_initialized():
            return []

        grid = self.load_data_grid()
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
