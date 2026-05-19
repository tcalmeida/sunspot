"""Angular utility functions for solar azimuth calculations."""


def angular_difference(a: float, b: float) -> float:
    """Return the minimum angular difference between two angles with wrap-around.

    Both angles are treated as degrees on a circle (0–360).
    The result is always in the range [0°, 180°].

    Args:
        a: First angle in degrees.
        b: Second angle in degrees.

    Returns:
        Minimum angular difference in degrees, always in [0, 180].
    """
    diff = abs(a - b) % 360.0
    return min(diff, 360.0 - diff)
