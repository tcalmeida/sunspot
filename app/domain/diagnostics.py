"""Domain diagnostics: solar exposure classification and recommendations.

No imports from streamlit, geopy or pvlib are allowed in this module.
"""

import datetime
import logging
from dataclasses import dataclass
from enum import Enum

import pandas as pd

from app.services.solar import SolarData
from app.utils.angle import angular_difference

logger = logging.getLogger(__name__)


class FacadeOrientation(Enum):
    """Eight-octant compass classification for facade orientation."""

    NORTE = "Norte"
    NORDESTE = "Nordeste"
    LESTE = "Leste (Sol da Manhã)"
    SUDESTE = "Sudeste"
    SUL = "Sul"
    SUDOESTE = "Sudoeste"
    OESTE = "Oeste (Sol da Tarde)"
    NOROESTE = "Noroeste"


@dataclass(slots=True)
class SunExposureResult:
    """Result of a solar exposure calculation for a given facade."""

    start_time: datetime.time | None
    end_time: datetime.time | None
    total_hours: float
    orientation: FacadeOrientation
    recommendations: list[str]
    has_sun: bool


def classify_orientation(azimuth: float) -> FacadeOrientation:
    """Classify facade orientation based on azimuth angle (0–360°).

    Divides the compass into eight 45°-wide octants centred on the
    cardinal and intercardinal directions.

    Args:
        azimuth: Window azimuth in degrees.  Any real number is accepted;
            it is normalised to [0°, 360°) internally.

    Returns:
        The matching FacadeOrientation enum member.
    """
    normalised = azimuth % 360.0

    if normalised < 22.5 or normalised >= 337.5:
        return FacadeOrientation.NORTE
    if normalised < 67.5:
        return FacadeOrientation.NORDESTE
    if normalised < 112.5:
        return FacadeOrientation.LESTE
    if normalised < 157.5:
        return FacadeOrientation.SUDESTE
    if normalised < 202.5:
        return FacadeOrientation.SUL
    if normalised < 247.5:
        return FacadeOrientation.SUDOESTE
    if normalised < 292.5:
        return FacadeOrientation.OESTE
    return FacadeOrientation.NOROESTE


def generate_recommendations(
    result: SunExposureResult, language: str = "English"
) -> list[str]:
    """Generate practical tips based on solar exposure and facade orientation.

    Args:
        result: A SunExposureResult (recommendations field may be empty).
        language: Language key for the output strings ("English" or "Português").

    Returns:
        A list of human-readable recommendation strings.
    """
    tips: list[str] = []
    en = language == "English"

    if not result.has_sun:
        if en:
            tips.append("This property receives no direct sunlight during this season.")
            tips.append(
                "Consider supplemental artificial lighting for interior spaces."
            )
            tips.append("Shade-tolerant plants are more suitable for this environment.")
        else:
            tips.append(
                "Este imóvel não recebe incidência direta de sol nesta época do ano."
            )
            tips.append(
                "Considere iluminação artificial complementar para ambientes internos."
            )
            tips.append(
                "Plantas que toleram sombra são mais adequadas para este espaço."
            )
        return tips

    orientation = result.orientation
    total_hours = result.total_hours

    # Orientation-specific tips
    if orientation == FacadeOrientation.LESTE:
        if en:
            tips.append("Great for those who enjoy morning light when waking up.")
            tips.append(
                "Afternoons stay cooler in summer, reducing air-conditioning use."
            )
            tips.append("Ideal for drying laundry in the morning.")
        else:
            tips.append("Ótimo para quem aprecia a luz da manhã ao acordar.")
            tips.append(
                "A tarde é mais fresca no verão, reduzindo o uso de ar-condicionado."
            )
            tips.append("Ideal para secar roupas pela manhã.")
    elif orientation == FacadeOrientation.OESTE:
        if en:
            tips.append("Receives strong sunlight in the afternoon.")
            tips.append("Can get very warm in summer — consider blinds or window film.")
            tips.append(
                "Good natural light for those who work from home in the afternoon."
            )
        else:
            tips.append("Recebe sol forte no período da tarde.")
            tips.append(
                "Pode aquecer bastante no verão — considere persianas ou películas."
            )
            tips.append("Boa iluminação natural para quem trabalha em casa à tarde.")
    elif orientation == FacadeOrientation.SUL:
        if en:
            tips.append(
                "South-facing facade receives little direct sunlight "
                "in the southern hemisphere."
            )
            tips.append("Spaces tend to be cooler with diffuse, even light.")
            tips.append(
                "Recommended for those who prefer environments without excessive heat."
            )
        else:
            tips.append("Fachada sul recebe pouca luz solar direta no hemisfério sul.")
            tips.append("Ambientes tendem a ser mais frescos e com luz difusa.")
            tips.append("Recomendado para quem prefere ambientes sem calor excessivo.")
    elif orientation == FacadeOrientation.NORTE:
        if en:
            tips.append(
                "North-facing facade receives sun for most of the day "
                "in the southern hemisphere."
            )
            tips.append("Excellent for natural heating in winter.")
            tips.append("Consider sun protection in summer to avoid overheating.")
        else:
            tips.append(
                "Fachada norte recebe sol durante boa parte do dia no hemisfério sul."
            )
            tips.append("Excelente para aquecimento natural no inverno.")
            tips.append(
                "Considere proteção solar no verão para evitar superaquecimento."
            )
    elif orientation == FacadeOrientation.NORDESTE:
        if en:
            tips.append("Receives morning sun with good intensity.")
            tips.append("Good balance between morning light and a milder afternoon.")
        else:
            tips.append("Recebe sol da manhã com boa intensidade.")
            tips.append("Equilibrio entre luz matinal e tarde mais amena.")
    elif orientation == FacadeOrientation.SUDESTE:
        if en:
            tips.append("Morning sun with softer intensity than northeast.")
            tips.append("Pleasant environment with gentle light during the morning.")
        else:
            tips.append("Sol da manhã com menor intensidade que o nordeste.")
            tips.append("Ambiente agradável com luz suave durante a manhã.")
    elif orientation == FacadeOrientation.SUDOESTE:
        if en:
            tips.append("Receives sun in the late afternoon.")
            tips.append("Can be warm in summer during the afternoon hours.")
        else:
            tips.append("Recebe sol no final da tarde.")
            tips.append("Pode ser quente no verão no período vespertino.")
    elif orientation == FacadeOrientation.NOROESTE:
        if en:
            tips.append("Strong sun in the late afternoon.")
            tips.append("Consider sun protection for windows facing this direction.")
        else:
            tips.append("Sol forte no final da tarde.")
            tips.append("Considere proteção solar para janelas nesta orientação.")

    # Exposure-duration tips
    if total_hours >= 6.0:
        if en:
            tips.append(
                f"Excellent sun exposure: {total_hours:.1f}h of direct"
                " sunlight per day."
            )
        else:
            tips.append(
                f"Excelente exposição solar: {total_hours:.1f}h de sol direto por dia."
            )
    elif total_hours >= 3.0:
        if en:
            tips.append(
                f"Good sun exposure: {total_hours:.1f}h of direct sunlight per day."
            )
        else:
            tips.append(
                f"Boa exposição solar: {total_hours:.1f}h de sol direto por dia."
            )
    else:
        if en:
            tips.append(
                f"Limited sun exposure: only {total_hours:.1f}h of direct"
                " sunlight per day."
            )
        else:
            tips.append(
                "Exposição solar limitada: apenas "
                f"{total_hours:.1f}h de sol direto por dia."
            )

    return tips


def calculate_sun_exposure(
    solar_data: SolarData,
    window_azimuth: float,
    angular_tolerance: float = 90.0,
    min_elevation: float = 5.0,
    language: str = "English",
) -> SunExposureResult:
    """Calculate solar exposure for a facade given its azimuth angle.

    Applies three sequential intersection filters:
    1. Nocturnal filter  – removes records where elevation <= 0°.
    2. Horizon filter    – removes records where elevation < min_elevation.
    3. Angular filter    – keeps records where the angular difference between
                           the sun's azimuth and the window azimuth is less
                           than angular_tolerance.

    Args:
        solar_data: Full-day solar position data from the solar service.
        window_azimuth: Facade/window azimuth in degrees (0–360).
        angular_tolerance: Half-width of the acceptance cone in degrees
            (default 90°, i.e. ±90° from the window normal).
        min_elevation: Minimum solar elevation above the horizon in degrees
            (default 5°).
        language: Language key for recommendation strings
            ("English" or "Português").

    Returns:
        SunExposureResult with exposure window, total hours, orientation
        and practical recommendations.
    """
    orientation = classify_orientation(window_azimuth)

    # Build a working DataFrame for vectorised filtering
    df = pd.DataFrame(
        {
            "azimuth": solar_data.azimuth.values,
            "elevation": solar_data.elevation.values,
        },
        index=solar_data.times,
    )

    # Filter 1: nocturnal – sun below the geometric horizon
    df = df[df["elevation"] > 0.0]

    # Filter 2: horizon – sun too low to clear typical obstructions
    df = df[df["elevation"] >= min_elevation]

    # Filter 3: angular – sun outside the facade's acceptance cone
    df = df[
        df["azimuth"].apply(
            lambda sun_az: angular_difference(sun_az, window_azimuth)
            < angular_tolerance
        )
    ]

    if df.empty:
        logger.debug(
            "No direct sun exposure for azimuth=%.1f° "
            "(tolerance=%.1f°, min_elev=%.1f°)",
            window_azimuth,
            angular_tolerance,
            min_elevation,
        )
        result = SunExposureResult(
            start_time=None,
            end_time=None,
            total_hours=0.0,
            orientation=orientation,
            recommendations=[],
            has_sun=False,
        )
        result.recommendations.extend(generate_recommendations(result, language))
        return result

    start_ts: pd.Timestamp = df.index[0]
    end_ts: pd.Timestamp = df.index[-1]

    # Total hours: number of intervals × interval duration in hours
    interval_minutes = _infer_interval_minutes(solar_data.times)
    total_hours = round(len(df) * interval_minutes / 60.0, 2)

    result = SunExposureResult(
        start_time=start_ts.time(),
        end_time=end_ts.time(),
        total_hours=total_hours,
        orientation=orientation,
        recommendations=[],
        has_sun=True,
    )
    result.recommendations.extend(generate_recommendations(result, language))
    return result


def _infer_interval_minutes(times: pd.DatetimeIndex) -> float:
    """Infer the sampling interval in minutes from a DatetimeIndex.

    Falls back to 10 minutes if the index has fewer than two entries.

    Args:
        times: Timezone-aware DatetimeIndex from SolarData.

    Returns:
        Interval duration in minutes as a float.
    """
    if len(times) < 2:
        return 10.0
    delta: pd.Timedelta = times[1] - times[0]
    return float(delta.total_seconds()) / 60.0
