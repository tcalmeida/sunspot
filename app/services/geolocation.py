"""Geocoding service: converts a textual address into geographic coordinates."""

import logging
from dataclasses import dataclass

from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
from geopy.location import Location

from app.config.settings import GEOCODING_TIMEOUT_SECONDS, NOMINATIM_USER_AGENT
from app.utils.exceptions import GeocodingError

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GeoLocation:
    latitude: float
    longitude: float
    formatted_address: str


def geocode_address(address: str) -> GeoLocation:
    """Convert a textual address into geographic coordinates.

    Args:
        address: Human-readable address string to geocode.

    Returns:
        GeoLocation with latitude, longitude and formatted address.

    Raises:
        GeocodingError: If the address is not found, the request times out,
            or the geocoding service is unavailable.
    """
    geocoder = Nominatim(user_agent=NOMINATIM_USER_AGENT)

    try:
        result: Location | None = geocoder.geocode(
            address, timeout=GEOCODING_TIMEOUT_SECONDS
        )
    except GeocoderTimedOut as exc:
        logger.warning("Geocoding timed out for address %r: %s", address, exc)
        raise GeocodingError(
            f"Geocoding request timed out for address: {address!r}"
        ) from exc
    except (GeocoderServiceError, GeocoderUnavailable) as exc:
        logger.error("Geocoding service error for address %r: %s", address, exc)
        raise GeocodingError(
            f"Geocoding service unavailable for address: {address!r}"
        ) from exc

    if result is None:
        logger.warning("Address not found: %r", address)
        raise GeocodingError(f"Address not found: {address!r}")

    return GeoLocation(
        latitude=float(result.latitude),
        longitude=float(result.longitude),
        formatted_address=str(result.address),
    )
