from pathlib import Path

import ee

from ee_collection_tracker.datasets._mgrs import MGRSDataset
from ee_collection_tracker.utils import initialize_service_account


class Sentinel2(MGRSDataset):
    label = "Sentinel-2"
    data_path = Path("site/data/sentinel2.csv")
    # The harmonized collections are more expensive to query due to on-the-processing. We query the
    # original collections and derive availability for the harmonized ones.
    collection_ids = (
        "COPERNICUS/S2",
        "COPERNICUS/S2_SR",
    )
    derived_collection_ids = {
        "COPERNICUS/S2": "COPERNICUS/S2_HARMONIZED",
        "COPERNICUS/S2_SR": "COPERNICUS/S2_SR_HARMONIZED",
    }
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
    initialize_service_account()
    Sentinel2().update()
