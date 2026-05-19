"""Custom exception hierarchy for the Sunspot application."""


class SunspotError(Exception):
    """Base exception for all Sunspot application errors.

    All domain-specific exceptions inherit from this class, allowing
    callers to catch any application error with a single except clause.
    """


class GeocodingError(SunspotError):
    """Raised when geocoding an address fails.

    Covers the following failure scenarios:
    - Address not found or ambiguous
    - Request timeout from the geocoding service
    - Geocoding service unavailable or returning an unexpected response
    """


class SolarCalculationError(SunspotError):
    """Raised when the solar position calculation fails.

    Covers the following failure scenarios:
    - Invalid or out-of-range coordinates passed to the calculation engine
    - Unexpected error from the underlying solar position library
    """
