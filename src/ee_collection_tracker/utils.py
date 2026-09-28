import json
import os
from pathlib import Path

import ee
import pandas as pd
from loguru import logger


def initialize_service_account():
    # Try service account data from the environment first
    credential_data = os.getenv("EE_SERVICE_ACCOUNT", "")
    if credential_data:
        logger.debug("Initializing Earth Engine with service account data.")
        credentials = ee.ServiceAccountCredentials(key_data=credential_data)
        project_id = json.loads(credential_data).get("project_id")
        ee.Initialize(credentials, project=project_id)
        return

    # Try a service account file next
    credential_path = Path(os.getenv("EE_SERVICE_ACCOUNT_PATH", "./service-account.json"))
    if credential_path.is_file():
        logger.debug("Initializing Earth Engine with service account key file.")
        credentials = ee.ServiceAccountCredentials(key_file=credential_path.as_posix())
        ee.Initialize(credentials)
        return

    # Try persistent credentials as a last resort
    logger.debug("Initializing Earth Engine with persistent credentials.")
    ee.Initialize("persistent")


def datetime_column_to_epoch_seconds(col: pd.Series) -> pd.Series:
    """Convert a datetime column to elapsed integer seconds since 1970-01-01."""
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    return (col - epoch).dt.total_seconds().astype(int)
