"""UI string translations for the Sunspot application."""

from typing import TypedDict


class Strings(TypedDict):
    subtitle: str
    address_label: str
    address_placeholder: str
    azimuth_label: str
    azimuth_help: str
    season_label: str
    season_summer: str
    season_winter: str
    button_calculate: str
    error_empty_address: str
    error_geocoding: str
    error_solar: str
    spinner: str
    result_header: str
    no_sun_warning: str
    metric_start: str
    metric_end: str
    metric_total: str
    facade_label: str
    recommendations_header: str


TRANSLATIONS: dict[str, Strings] = {
    "Português": {
        "subtitle": "Descubra o sol do seu próximo lar",
        "address_label": "📍 Endereço do imóvel",
        "address_placeholder": "Ex: Rua das Flores, 123, São Paulo, SP",
        "azimuth_label": "🧭 Ângulo da janela principal (azimute)",
        "azimuth_help": "0° = Norte, 90° = Leste, 180° = Sul, 270° = Oeste",
        "season_label": "📅 Época do ano",
        "season_summer": "Verão",
        "season_winter": "Inverno",
        "button_calculate": "Calcular Incidência Solar",
        "error_empty_address": "Por favor, informe o endereço do imóvel.",
        "error_geocoding": (
            "Endereço não encontrado. Verifique o endereço e tente novamente."
        ),
        "error_solar": (
            "Erro ao calcular a posição solar. Tente novamente mais tarde."
        ),
        "spinner": "Calculando...",
        "result_header": "☀️ Resultado",
        "no_sun_warning": (
            "Este imóvel não recebe incidência direta de sol nesta época do ano."
        ),
        "metric_start": "Início",
        "metric_end": "Fim",
        "metric_total": "Total",
        "facade_label": "🧭 Fachada:",
        "recommendations_header": "💡 Recomendações",
    },
    "English": {
        "subtitle": "Discover the sunlight in your next home",
        "address_label": "📍 Property address",
        "address_placeholder": "e.g. 123 Main St, New York, NY",
        "azimuth_label": "🧭 Main window angle (azimuth)",
        "azimuth_help": "0° = North, 90° = East, 180° = South, 270° = West",
        "season_label": "📅 Season",
        "season_summer": "Summer",
        "season_winter": "Winter",
        "button_calculate": "Calculate Sun Exposure",
        "error_empty_address": "Please enter the property address.",
        "error_geocoding": (
            "Address not found. Please check the address and try again."
        ),
        "error_solar": "Error calculating solar position. Please try again later.",
        "spinner": "Calculating...",
        "result_header": "☀️ Result",
        "no_sun_warning": (
            "This property receives no direct sunlight during this season."
        ),
        "metric_start": "Start",
        "metric_end": "End",
        "metric_total": "Total",
        "facade_label": "🧭 Facade:",
        "recommendations_header": "💡 Recommendations",
    },
}
