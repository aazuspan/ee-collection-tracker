"""
HLS datasets (HLSS and HLSL) for Earth Engine collection tracking.

These are stored as separate datasets rather than a single dataset with two collections
because they query slightly differently due to different start years and properties.
However, they still write into the same output file as if they were a shared collection.
"""

from pathlib import Path

import ee
from loguru import logger

from ee_collection_tracker.datasets._mgrs import MGRSDataset
from ee_collection_tracker.utils import initialize_service_account


class HLSS(MGRSDataset):
    label = "HLS"
    collection_ids = ("NASA/HLS/HLSS30/v002_RAW2",)
    derived_collection_ids = {
        "NASA/HLS/HLSS30/v002_RAW2": "NASA/HLS/HLSS30/v002",
    }
    data_path = Path("site/data/hls.csv")
    _mgrs_property: str = "MGRS_TILE_ID"
    _mgrs_column: str = "MGRS_TILE"
    _start_year = 2015
    index_dtypes = {"MGRS_TILE": "str"}


class HLSL(MGRSDataset):
    label = "HLS"
    collection_ids = ("NASA/HLS/HLSL30/v002_RAW2",)
    derived_collection_ids = {
        "NASA/HLS/HLSL30/v002_RAW2": "NASA/HLS/HLSL30/v002",
    }
    data_path = Path("site/data/hls.csv")
    _mgrs_property: str = "MGRS_TILE_ID"
    _mgrs_column: str = "MGRS_TILE"
    _start_year = 2013
    index_dtypes = {"MGRS_TILE": "str"}

    def _get_collection(self, collection_id: str) -> ee.ImageCollection:
        def _assign_mgrs_property(image: ee.Image) -> ee.Image:
            # HLSL doesn't have an explicit MGRS tile property, but it does store the MGRS tile ID
            # in the system:index property between characters 1 and 6, which we can parse.
            # For example: "T01FBE_20130814T214019" -> "01FBE"
            return image.set({self._mgrs_property: image.getString("system:index").slice(1, 6)})

        return super()._get_collection(collection_id).map(_assign_mgrs_property)


def update_hls():
    logger.info("Initializing service account")
    initialize_service_account()

    logger.info("Updating HLSL")
    HLSL().update()

    logger.info("Updating HLSS")
    HLSS().update()
