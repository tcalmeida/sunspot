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
from app.utils.exceptions import GeocodingError, SolarCalculationError

logger = logging.getLogger(__name__)


def render_inputs() -> tuple[str, float, str]:
    """Render the input widgets and return user-provided values.

    Returns:
        A tuple of (address, window_azimuth, season) where season is
        either "Verão" or "Inverno".
    """
    address: str = st.text_input(
        "📍 Endereço do imóvel",
        placeholder="Ex: Rua das Flores, 123, São Paulo, SP",
    )

    window_azimuth: float = float(
        st.slider(
            "🧭 Ângulo da janela principal (azimute)",
            min_value=0,
            max_value=359,
            value=90,
            step=1,
            help="0° = Norte, 90° = Leste, 180° = Sul, 270° = Oeste",
        )
    )

    season: str = st.radio(
        "📅 Época do ano",
        options=["Verão", "Inverno"],
        horizontal=True,
    )  # type: ignore[assignment]

    return address, window_azimuth, season


def render_results(result: SunExposureResult) -> None:
    """Display solar exposure metrics, orientation and recommendations.

    Args:
        result: Computed solar exposure result to display.
    """
    st.divider()
    st.subheader("☀️ Resultado")

    if not result.has_sun:
        st.warning(
            "Este imóvel não recebe incidência direta de sol nesta época do ano."
        )
    else:
        start_str = result.start_time.strftime("%H:%M") if result.start_time else "—"
        end_str = result.end_time.strftime("%H:%M") if result.end_time else "—"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Início", start_str)
        with col2:
            st.metric("Fim", end_str)
        with col3:
            hours = int(result.total_hours)
            minutes = round((result.total_hours - hours) * 60)
            st.metric("Total", f"{hours}h {minutes:02d}m")

    st.markdown(f"**🧭 Fachada:** {result.orientation.value}")

    if result.recommendations:
        st.subheader("💡 Recomendações")
        for tip in result.recommendations:
            st.markdown(f"• {tip}")


def render_error(message: str) -> None:
    """Display a user-friendly error message.

    Args:
        message: Human-readable error description to show.
    """
    st.error(f"❌ {message}")


def render_main_page() -> None:
    """Render the full main page: inputs, calculation trigger and results."""
    st.title("☀️ Sunspot")
    st.subheader("Descubra o sol do seu próximo lar")

    address, window_azimuth, season = render_inputs()

    if st.button("Calcular Incidência Solar", type="primary"):
        if not address.strip():
            render_error("Por favor, informe o endereço do imóvel.")
            return

        date: datetime.date = SUMMER_SOLSTICE if season == "Verão" else WINTER_SOLSTICE

        with st.spinner("Calculando..."):
            try:
                location = geocode_address(address)
            except GeocodingError as exc:
                logger.warning("Geocoding failed for %r: %s", address, exc)
                render_error(
                    "Endereço não encontrado. Verifique o endereço e tente novamente."
                )
                return

            try:
                solar_data = calculate_solar_position(
                    latitude=location.latitude,
                    longitude=location.longitude,
                    date=date,
                )
            except SolarCalculationError as exc:
                logger.error("Solar calculation failed: %s", exc)
                render_error(
                    "Erro ao calcular a posição solar. Tente novamente mais tarde."
                )
                return

            result = calculate_sun_exposure(
                solar_data=solar_data,
                window_azimuth=window_azimuth,
                angular_tolerance=ANGULAR_TOLERANCE_DEGREES,
                min_elevation=MIN_SOLAR_ELEVATION_DEGREES,
            )

        render_results(result)
