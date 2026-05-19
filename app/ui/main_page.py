"""Main page UI components for the Sunspot Streamlit application."""

import datetime
import logging

import streamlit as st

from app.config.settings import (
    ANGULAR_TOLERANCE_DEGREES,
    MIN_SOLAR_ELEVATION_DEGREES,
    SUMMER_SOLSTICE,
    WINTER_SOLSTICE,
)
from app.domain.diagnostics import SunExposureResult, calculate_sun_exposure
from app.services.geolocation import geocode_address
from app.services.solar import calculate_solar_position
from app.ui.i18n import TRANSLATIONS, Strings
from app.utils.exceptions import GeocodingError, SolarCalculationError

logger = logging.getLogger(__name__)

_LANGUAGES = list(TRANSLATIONS.keys())


def _get_strings() -> Strings:
    """Return the string set for the currently selected language."""
    lang: str = st.session_state.get("language", "Português")
    return TRANSLATIONS[lang]


def render_language_selector() -> None:
    """Render the language toggle in the sidebar."""
    st.sidebar.selectbox(
        "🌐 Language / Idioma",
        options=_LANGUAGES,
        key="language",
    )


def render_inputs(s: Strings) -> tuple[str, float, str]:
    """Render the input widgets and return user-provided values.

    Args:
        s: Localized string set.

    Returns:
        A tuple of (address, window_azimuth, season_key) where season_key
        is the localized summer or winter label.
    """
    address: str = st.text_input(
        s["address_label"],
        placeholder=s["address_placeholder"],
    )

    window_azimuth: float = float(
        st.slider(
            s["azimuth_label"],
            min_value=0,
            max_value=359,
            value=90,
            step=1,
            help=s["azimuth_help"],
        )
    )

    season: str = st.radio(
        s["season_label"],
        options=[s["season_summer"], s["season_winter"]],
        horizontal=True,
    )  # type: ignore[assignment]

    return address, window_azimuth, season


def render_results(result: SunExposureResult, s: Strings) -> None:
    """Display solar exposure metrics, orientation and recommendations.

    Args:
        result: Computed solar exposure result to display.
        s: Localized string set.
    """
    st.divider()
    st.subheader(s["result_header"])

    if not result.has_sun:
        st.warning(s["no_sun_warning"])
    else:
        start_str = result.start_time.strftime("%H:%M") if result.start_time else "—"
        end_str = result.end_time.strftime("%H:%M") if result.end_time else "—"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(s["metric_start"], start_str)
        with col2:
            st.metric(s["metric_end"], end_str)
        with col3:
            hours = int(result.total_hours)
            minutes = round((result.total_hours - hours) * 60)
            st.metric(s["metric_total"], f"{hours}h {minutes:02d}m")

    st.markdown(f"**{s['facade_label']}** {result.orientation.value}")

    if result.recommendations:
        st.subheader(s["recommendations_header"])
        for tip in result.recommendations:
            st.markdown(f"• {tip}")


def render_error(message: str) -> None:
    """Display a user-friendly error message.

    Args:
        message: Human-readable error description to show.
    """
    st.error(f"❌ {message}")


def render_main_page() -> None:
    """Render the full main page: language selector, inputs, calculation and results."""
    render_language_selector()

    s = _get_strings()

    st.title("☀️ Sunspot")
    st.subheader(s["subtitle"])

    address, window_azimuth, season = render_inputs(s)

    if st.button(s["button_calculate"], type="primary"):
        if not address.strip():
            render_error(s["error_empty_address"])
            return

        is_summer = season == s["season_summer"]
        date: datetime.date = SUMMER_SOLSTICE if is_summer else WINTER_SOLSTICE

        with st.spinner(s["spinner"]):
            try:
                location = geocode_address(address)
            except GeocodingError as exc:
                logger.warning("Geocoding failed for %r: %s", address, exc)
                render_error(s["error_geocoding"])
                return

            try:
                solar_data = calculate_solar_position(
                    latitude=location.latitude,
                    longitude=location.longitude,
                    date=date,
                )
            except SolarCalculationError as exc:
                logger.error("Solar calculation failed: %s", exc)
                render_error(s["error_solar"])
                return

            result = calculate_sun_exposure(
                solar_data=solar_data,
                window_azimuth=window_azimuth,
                angular_tolerance=ANGULAR_TOLERANCE_DEGREES,
                min_elevation=MIN_SOLAR_ELEVATION_DEGREES,
            )

        render_results(result, s)
