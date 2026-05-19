"""Solar position service: calculates sun azimuth and elevation for a full day."""

import datetime
import logging
from dataclasses import dataclass

import pandas as pd
import pvlib.solarposition

from app.config.settings import SOLAR_INTERVAL_MINUTES
from app.utils.exceptions import SolarCalculationError

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SolarData:
    times: pd.DatetimeIndex
    azimuth: pd.Series    # degrees, 0–360
    elevation: pd.Series  # degrees, -90 to 90


def calculate_solar_position(
    latitude: float,
    longitude: float,
    date: datetime.date,
    interval_minutes: int = SOLAR_INTERVAL_MINUTES,
) -> SolarData:
    """Calculate solar azimuth and elevation for every interval of the given day.

    Args:
        latitude: Geographic latitude in decimal degrees (-90 to 90).
        longitude: Geographic longitude in decimal degrees (-180 to 180).
        date: The calendar date for which to compute solar positions.
        interval_minutes: Time resolution in minutes (default from settings).

    Returns:
        SolarData with timezone-aware times, azimuth and elevation series.

    Raises:
        SolarCalculationError: If the calculation fails for any reason.
    """
    try:
        start = pd.Timestamp(year=date.year, month=date.month, day=date.day, tz="UTC")
        end = start + pd.Timedelta(hours=23, minutes=59)
        times: pd.DatetimeIndex = pd.date_range(
            start=start,
            end=end,
            freq=f"{interval_minutes}min",
        )

        solar_position: pd.DataFrame = pvlib.solarposition.get_solarposition(
            times, latitude, longitude
        )

        elevation_col = (
            "apparent_elevation"
            if "apparent_elevation" in solar_position.columns
            else "elevation"
        )

        return SolarData(
            times=times,
            azimuth=solar_position["azimuth"],
            elevation=solar_position[elevation_col],
        )
    except Exception as exc:
        logger.error(
            "Solar position calculation failed for lat=%s, lon=%s, date=%s: %s",
            latitude,
            longitude,
            date,
            exc,
        )
        raise SolarCalculationError(
            f"Failed to calculate solar position for coordinates "
            f"({latitude}, {longitude}) on {date}: {exc}"
        ) from exc
