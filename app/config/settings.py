"""Application constants and configuration settings."""

import datetime
import logging
import os

logger = logging.getLogger(__name__)

APP_NAME: str = "Sunspot"

NOMINATIM_USER_AGENT: str = os.environ.get("NOMINATIM_USER_AGENT", "sunspot-mvp")

GEOCODING_TIMEOUT_SECONDS: int = 10
SOLAR_INTERVAL_MINUTES: int = 10
MIN_SOLAR_ELEVATION_DEGREES: float = 5.0
ANGULAR_TOLERANCE_DEGREES: float = 90.0

# Solstice dates — hemisphere-aware
# Northern hemisphere: summer = June, winter = December
# Southern hemisphere: summer = December, winter = June
SOLSTICE_JUNE: datetime.date = datetime.date(2024, 6, 21)
SOLSTICE_DECEMBER: datetime.date = datetime.date(2024, 12, 21)
