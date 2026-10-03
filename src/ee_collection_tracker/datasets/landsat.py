from pathlib import Path

import ee
import pandas as pd
from loguru import logger

from ee_collection_tracker.datasets._dataset import TIME_START_COL, Dataset
from ee_collection_tracker.utils import initialize_service_account

# WRS-2 has 233 paths and 122 rows for descending day-time orbits. Ascending night-
# time orbits are in rows 123-248.
_WRS2_PATHS = 233
_WRS2_DAY_ROWS = 122

# Column names for the state DataFrame.
_PATH_COL = "PATH"
_ROW_COL = "ROW"


class Landsat(Dataset):
    label = "Landsat"
    data_path = Path("site/data/landsat.csv")
    grid_path = Path("site/data/grid/wrs2.geojson")
    feature_label = "Path {PATH}, Row {ROW}"
    collection_ids = (
        "LANDSAT/LC08/C02/T1",
        "LANDSAT/LC08/C02/T1_L2",
        "LANDSAT/LC09/C02/T1",
        "LANDSAT/LC09/C02/T1_L2",
    )
    # TOA collections are derived on-the-fly from the Level 1 raw collections, which makes them
    # more expensive to query, so we only track the raw collections.
    derived_collection_ids = {
        "LANDSAT/LC08/C02/T1": "LANDSAT/LC08/C02/T1_TOA",
        "LANDSAT/LC09/C02/T1": "LANDSAT/LC09/C02/T1_TOA",
    }
    index_dtypes = {_PATH_COL: "uint8", _ROW_COL: "uint8"}

    def _get_collection(self, collection_id: str) -> ee.ImageCollection:
        # Exclude nighttime acquisitions which are in rows 123-248
        return (
            super()
            ._get_collection(collection_id)
            .filter(ee.Filter.lt("WRS_ROW", _WRS2_DAY_ROWS + 1))
        )

    def _chunks(self, chunk_size: int = 10) -> list[tuple[int, int]]:
        """Split WRS-2 paths into inclusive (start, end) chunks.

        Landsat queries are efficient enough that you can grab entire collections without
        chunking, but chunking on 10 paths at once was consistently faster in my testing.
        """
        return [
            (start, min(start + chunk_size - 1, _WRS2_PATHS))
            for start in range(1, _WRS2_PATHS + 1, chunk_size)
        ]

    def _query_chunk(self, collection: ee.ImageCollection, start: int, end: int) -> pd.DataFrame:
        """Query the latest daytime asset for each path/row in an inclusive path range."""
        latest = (
            collection.filter(ee.Filter.rangeContains("WRS_PATH", start, end))
            .sort("system:time_start", False)
            .distinct(["WRS_PATH", "WRS_ROW"])
            .map(_get_landsat_metadata)
        )
        features = ee.data.computeFeatures({"expression": latest, "fileFormat": "PANDAS_DATAFRAME"})
        return features.drop(columns=["geo"], errors="ignore")


def _get_landsat_metadata(image: ee.Image) -> ee.Feature:
    """Convert a Landsat image to a minimal metadata feature."""
    return ee.Feature(
        None,
        {
            # ee.Image.toDictionary() is a little more efficient, but
            # ee.data.computeFeatures apparently drops system properties, so we need to
            # rename manually.
            TIME_START_COL: image.get("system:time_start"),
            _PATH_COL: image.get("WRS_PATH"),
            _ROW_COL: image.get("WRS_ROW"),
        },
    )


def update_landsat():
    logger.info("Initializing service account")
    initialize_service_account()

    logger.info("Updating Landsat")
    Landsat().update()
