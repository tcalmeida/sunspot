"""Season-to-date resolution utilities."""

import datetime

from app.config.settings import SOLSTICE_DECEMBER, SOLSTICE_JUNE


def resolve_solstice_date(is_summer: bool, latitude: float) -> datetime.date:
    """Return the solstice date that matches the requested season and hemisphere.

    In the Southern hemisphere (latitude < 0) summer falls in December;
    in the Northern hemisphere summer falls in June.

    Args:
        is_summer: True if the user selected summer, False for winter.
        latitude: Geographic latitude of the property (-90 to 90).

    Returns:
        The solstice date corresponding to the requested season.
    """
    southern = latitude < 0
    if is_summer:
        return SOLSTICE_DECEMBER if southern else SOLSTICE_JUNE
    return SOLSTICE_JUNE if southern else SOLSTICE_DECEMBER
