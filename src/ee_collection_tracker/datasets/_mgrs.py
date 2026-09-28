from abc import ABC
from datetime import UTC, datetime
from pathlib import Path

import ee
import pandas as pd

from ee_collection_tracker.datasets._dataset import TIME_START_COL, Dataset


class MGRSDataset(Dataset, ABC):
    """A dataset that's indexed on the MGRS grid and queried by year.

    This includes Sentinel-2 and HLS.
    """

    data_path: Path
    collection_ids: tuple[str, ...]
    grid_path = Path("site/data/grid/mgrs.geojson")
    feature_label = "{MGRS_TILE}"

    # Because MGRS is chunked by year, we need to know where to start querying during initialization
    _start_year: int

    # The MGRS property in Earth Engine and the MGRS column in the local output differ because
    # different collections store different properties, but they need to match locally.
    # Sentinel-2 stores "MGRS_TILE", but HLSS stores "MGRS_TILE_ID".
    _mgrs_property: str
    _mgrs_column: str
    index_dtypes: dict[str, str]

    def _chunks(self, chunk_size: int = 1) -> list[tuple[int, int]]:
        """Split the query period into inclusive (start, end) year chunks ending this year.

        I tried a number of different approaches including spatial chunking, filtering MGRS by
        prefix using stringStartsWith, and filtering on lists of MGRS tiles using inList.
        The grouped reducer is by far the fastest approach, but still requires some temporal
        chunking to avoid computations timing out. Temporal chunking is inherently inefficient
        since you're querying old assets that will mostly be replaced with newer assets, but
        it ensures an exhaustive search.
        """
        end_year = datetime.now(UTC).year
        # For an update query, just look back one year. For a full initialization, start from
        # the first acquisition year
        start_year = end_year - 1 if self.is_initialized() else self._start_year
        return [
            (start, min(start + chunk_size - 1, end_year))
            for start in range(start_year, end_year + 1, chunk_size)
        ]

    def _query_chunk(self, collection: ee.ImageCollection, start: int, end: int) -> pd.DataFrame:
        """Query the latest descending asset per MGRS tile in an inclusive year range."""
        latest = collection.filter(ee.Filter.calendarRange(start, end, "year")).reduceColumns(
            ee.Reducer.max().group(
                groupField=1,
                groupName=self._mgrs_property,
            ),
            ["system:time_start", self._mgrs_property],
        )
        groups = latest.getInfo().get("groups", [])
        # Rename the grouped max property to a time column and the MGRS property in EE to the
        # MGRS column used in the template grid.
        return pd.DataFrame(groups, columns=["max", self._mgrs_property]).rename(
            columns={"max": TIME_START_COL, self._mgrs_property: self._mgrs_column}
        )
