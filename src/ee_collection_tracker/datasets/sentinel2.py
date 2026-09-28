from pathlib import Path

import ee
from loguru import logger

from ee_collection_tracker.datasets._mgrs import MGRSDataset
from ee_collection_tracker.utils import initialize_service_account


class Sentinel2(MGRSDataset):
    label = "Sentinel-2"
    data_path = Path("site/data/sentinel2.csv")
    # These are technically deprecated, but the harmonized collections that "replaced" them are
    # actually derived from them on-the-fly, which makes them much more expensive to query. We can
    # fully determine availability from the original collections.
    collection_ids = (
        "COPERNICUS/S2",
        "COPERNICUS/S2_SR",
    )
    _mgrs_property: str = "MGRS_TILE"
    _mgrs_column: str = "MGRS_TILE"
    _start_year = 2015
    index_dtypes = {"MGRS_TILE": "str"}

    def _get_collection(self, collection_id: str) -> ee.ImageCollection:
        # Remove ascending night-time passes
        return (
            super()
            ._get_collection(collection_id)
            .filter(ee.Filter.eq("SENSING_ORBIT_DIRECTION", "DESCENDING"))
        )


def update_sentinel2():
    logger.info("Initializing service account")
    initialize_service_account()

    logger.info("Updating Sentinel-2")
    Sentinel2().update()
