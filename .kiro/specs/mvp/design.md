# Design Document

## Overview

O Sunspot é uma aplicação web leve construída com Python e Streamlit. O usuário informa um endereço e o ângulo da janela do imóvel; a aplicação geocodifica o endereço, calcula a trajetória solar do dia e retorna os horários de incidência direta de sol, o total de horas e um diagnóstico prático em linguagem acessível.

A arquitetura é intencionalmente simples e desacoplada: a interface Streamlit não conhece as regras de negócio, e os módulos de domínio não conhecem o Streamlit. Isso permite trocar o frontend no futuro sem reescrever a lógica central.

---

## Architecture

### Visão Geral

```
┌─────────────────────────────────────────────────────┐
│                    app.py (entry point)              │
│              Streamlit bootstrap + routing           │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   app/ui/                            │
│         Componentes e páginas Streamlit              │
│   (inputs, resultados, loading, mensagens de erro)   │
└──────────────────────┬──────────────────────────────┘
                       │ chama
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌─────────▼──────────┐
│ app/services/  │          │   app/services/    │
│ geolocation.py │          │     solar.py       │
│  (geopy)       │          │     (pvlib)        │
└───────┬────────┘          └─────────┬──────────┘
        │                             │
        └──────────────┬──────────────┘
                       │ dados brutos
┌──────────────────────▼──────────────────────────────┐
│                 app/domain/                          │
│               diagnostics.py                        │
│   (interseção angular, classificação, diagnóstico)   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                 app/utils/ + app/config/             │
│        Constantes, helpers, configurações            │
└─────────────────────────────────────────────────────┘
```

### Camadas

| Camada | Localização | Responsabilidade |
|--------|-------------|-----------------|
| UI | `app/ui/` | Renderizar interface, capturar inputs, exibir resultados |
| Services | `app/services/` | Integração com APIs externas (geopy, pvlib) |
| Domain | `app/domain/` | Regras de negócio puras, sem dependência de frameworks |
| Utils | `app/utils/` | Funções auxiliares reutilizáveis |
| Config | `app/config/` | Constantes, configurações e variáveis de ambiente |

---

## Components and Interfaces

### `app/services/geolocation.py`

Responsável por converter um endereço em coordenadas geográficas.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class GeoLocation:
    latitude: float
    longitude: float
    formatted_address: str

def geocode_address(address: str) -> GeoLocation:
    """
    Converte um endereço textual em coordenadas geográficas.
    Raises: GeocodingError se o endereço não for encontrado ou timeout.
    """
    ...
```

**Dependência:** `geopy.geocoders.Nominatim`
**Erros tratados:** endereço não encontrado, timeout, serviço indisponível

---

### `app/services/solar.py`

Responsável por calcular a posição solar ao longo de um dia completo.

```python
import pandas as pd
from dataclasses import dataclass

@dataclass(slots=True)
class SolarData:
    times: pd.DatetimeIndex
    azimuth: pd.Series   # graus, 0–360
    elevation: pd.Series # graus, -90 a 90

def calculate_solar_position(
    latitude: float,
    longitude: float,
    date: datetime.date,
    interval_minutes: int = 10,
) -> SolarData:
    """
    Calcula azimute e elevação solar para cada intervalo do dia.
    Retorna série temporal com resolução de `interval_minutes`.
    """
    ...
```

**Dependência:** `pvlib.solarposition.get_solarposition`, `pandas.date_range`

---

### `app/domain/diagnostics.py`

Núcleo de regras de negócio. Não importa Streamlit, geopy nem pvlib diretamente.

```python
from dataclasses import dataclass
from enum import Enum

class FacadeOrientation(Enum):
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
    start_time: datetime.time | None
    end_time: datetime.time | None
    total_hours: float
    orientation: FacadeOrientation
    recommendations: list[str]
    has_sun: bool

def calculate_sun_exposure(
    solar_data: SolarData,
    window_azimuth: float,
    angular_tolerance: float = 90.0,
    min_elevation: float = 5.0,
) -> SunExposureResult:
    """
    Cruza a trajetória solar com o ângulo da janela e retorna
    o diagnóstico de exposição solar do imóvel.
    """
    ...

def classify_orientation(azimuth: float) -> FacadeOrientation:
    """Classifica a orientação da fachada com base no ângulo (0–360°)."""
    ...

def generate_recommendations(result: SunExposureResult) -> list[str]:
    """Gera dicas práticas baseadas na exposição e orientação."""
    ...
```

---

### `app/ui/main_page.py`

Componente principal da interface Streamlit.

```python
def render_main_page() -> None:
    """Renderiza a página principal com inputs e resultados."""
    ...

def render_inputs() -> tuple[str, float, str]:
    """Retorna (address, window_azimuth, season)."""
    ...

def render_results(result: SunExposureResult) -> None:
    """Exibe métricas, diagnóstico e recomendações."""
    ...

def render_error(message: str) -> None:
    """Exibe mensagem de erro amigável."""
    ...
```

---

### `app/config/settings.py`

```python
APP_NAME: str = "Sunspot"
NOMINATIM_USER_AGENT: str = "sunspot-mvp"
GEOCODING_TIMEOUT_SECONDS: int = 10
SOLAR_INTERVAL_MINUTES: int = 10
MIN_SOLAR_ELEVATION_DEGREES: float = 5.0
ANGULAR_TOLERANCE_DEGREES: float = 90.0

SUMMER_SOLSTICE: datetime.date = datetime.date(2024, 12, 21)  # Hemisfério Sul
WINTER_SOLSTICE: datetime.date = datetime.date(2024, 6, 21)   # Hemisfério Sul
```

---

## Data Models

### Fluxo de dados

```
Usuário
  │
  ├─ address: str          → GeoLocation(lat, lon, formatted_address)
  ├─ window_azimuth: float │
  └─ season: str           → date (solstício de verão ou inverno)
                           │
                           ▼
                    SolarData(times, azimuth, elevation)
                           │
                           ▼
                    SunExposureResult(
                        start_time, end_time,
                        total_hours, orientation,
                        recommendations, has_sun
                    )
                           │
                           ▼
                    UI (métricas + diagnóstico)
```

### Regras de Classificação de Orientação

| Ângulo da Janela | Orientação |
|-----------------|------------|
| 337.5° – 22.5°  | Norte |
| 22.5° – 67.5°   | Nordeste |
| 67.5° – 112.5°  | Leste (Sol da Manhã) |
| 112.5° – 157.5° | Sudeste |
| 157.5° – 202.5° | Sul |
| 202.5° – 247.5° | Sudoeste |
| 247.5° – 292.5° | Oeste (Sol da Tarde) |
| 292.5° – 337.5° | Noroeste |

### Regras de Interseção Solar

1. **Filtro noturno:** eliminar registros com `elevation <= 0°`
2. **Filtro de horizonte:** eliminar registros com `elevation < MIN_SOLAR_ELEVATION_DEGREES` (padrão 5°)
3. **Filtro angular:** manter registros onde `|azimuth_sol - azimuth_janela| < ANGULAR_TOLERANCE_DEGREES` (padrão 90°)
4. **Resultado:** primeiro e último registro válido definem `start_time` e `end_time`

---

## Error Handling

| Situação | Comportamento |
|----------|--------------|
| Endereço não encontrado | Exibe mensagem amigável, não propaga exceção para UI |
| Timeout do Nominatim | Exibe mensagem de retry, sugere verificar conexão |
| Nenhum sol no dia | `has_sun = False`, exibe mensagem explicativa |
| Input inválido (azimute fora de 0–360°) | Validação no frontend antes de chamar serviços |
| Erro inesperado | Log com `logger.exception`, mensagem genérica na UI |

Hierarquia de exceções customizadas:

```python
class SunspotError(Exception): ...
class GeocodingError(SunspotError): ...
class SolarCalculationError(SunspotError): ...
```

---

## Project Structure

```text
sunspot/
├── app.py                        # Entry point: streamlit run app.py
├── requirements.txt              # Todas as dependências (runtime + qualidade)
├── pyproject.toml                # Configuração de ruff, black, mypy
├── .env.example
│
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_page.py          # Componentes Streamlit
│   ├── services/
│   │   ├── __init__.py
│   │   ├── geolocation.py        # Integração geopy
│   │   └── solar.py              # Integração pvlib
│   ├── domain/
│   │   ├── __init__.py
│   │   └── diagnostics.py        # Regras de negócio
│   ├── utils/
│   │   ├── __init__.py
│   │   └── angle.py              # Helpers de cálculo angular
│   └── config/
│       ├── __init__.py
│       └── settings.py           # Constantes e configurações
│
└── tests/                        # Criado sob demanda do usuário
    ├── unit/
    └── integration/
```

---

## UI Layout

```
┌─────────────────────────────────────────┐
│  ☀️  Sunspot                             │
│  Descubra o sol do seu próximo lar       │
├─────────────────────────────────────────┤
│                                         │
│  📍 Endereço do imóvel                  │
│  [________________________________]     │
│                                         │
│  🧭 Ângulo da janela principal          │
│  [slider 0° ──────●────────── 360°]     │
│                                         │
│  📅 Época do ano                        │
│  ( ) Verão  ( ) Inverno                 │
│                                         │
│  [    Calcular Incidência Solar    ]     │
│                                         │
├─────────────────────────────────────────┤
│  RESULTADO                              │
│                                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Início   │ │  Fim     │ │  Total  │ │
│  │  07:20   │ │  13:40   │ │ 6h 20m  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│                                         │
│  🧭 Fachada: Leste (Sol da Manhã)       │
│                                         │
│  💡 Recomendações                       │
│  • Ótimo para quem acorda cedo          │
│  • Tarde mais fresca no verão           │
│  • Ideal para secar roupas pela manhã   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Notes

- O `app.py` é apenas o ponto de entrada do Streamlit; toda lógica fica nos módulos internos.
- A separação entre `services/` e `domain/` garante que as regras de negócio possam ser testadas sem dependência de rede.
- O `pyproject.toml` centraliza a configuração de ruff, black e mypy para evitar arquivos de config dispersos.
- Testes serão criados sob demanda do usuário, após a aplicação estar funcionando.

---

## Correctness Properties

As seguintes propriedades devem ser verdadeiras em qualquer execução correta da aplicação:

### Property 1: Geocodificação válida

Dado um endereço válido, `geocode_address` sempre retorna latitude no intervalo `[-90, 90]` e longitude no intervalo `[-180, 180]`.

**Validates: Requirements 1.1**

### Property 2: Posição solar dentro dos limites

`elevation` está sempre no intervalo `[-90°, 90°]` e `azimuth` no intervalo `[0°, 360°)` para qualquer entrada válida de coordenadas e data.

**Validates: Requirements 1.2**

### Property 3: Consistência temporal

Quando `has_sun = True`, `start_time` é sempre anterior a `end_time` e `total_hours > 0`.

**Validates: Requirements 1.3**

### Property 4: Total de horas dentro do limite

`total_hours >= 0` e nunca excede 24, independentemente da localização ou época do ano.

**Validates: Requirements 1.3**

### Property 5: Classificação de orientação completa

Todo valor de `window_azimuth` no intervalo `[0°, 360°)` mapeia para exatamente uma `FacadeOrientation`, sem lacunas nem sobreposições.

**Validates: Requirements 1.4**

### Property 6: Estado sem sol consistente

Quando nenhum registro passa pelos filtros de interseção, `has_sun = False`, `start_time = None` e `end_time = None`.

**Validates: Requirements 1.3**

### Property 7: Isolamento de domínio

Nenhum módulo em `app/domain/` importa `streamlit`, `geopy` ou `pvlib` diretamente, garantindo que as regras de negócio sejam independentes de frameworks externos.

**Validates: Requirements 1.5**

---

## Testing Strategy

> **Atenção:** os testes serão criados sob demanda explícita do usuário, após a aplicação estar funcionando. Esta seção documenta a estratégia planejada para quando forem solicitados.

### Testes Unitários (`tests/unit/`)

| Módulo | O que testar |
|--------|-------------|
| `domain/diagnostics.py` | Classificação de orientação para todos os octantes, cálculo de `total_hours`, comportamento com `has_sun = False`, geração de recomendações |
| `utils/angle.py` | Diferença angular com wrap-around (ex: 350° vs 10°) |
| `services/solar.py` | Formato e tipos do `SolarData` retornado (mock do pvlib) |
| `services/geolocation.py` | Tratamento de `GeocodingError` em timeout e endereço inválido (mock do Nominatim) |

### Testes de Integração (`tests/integration/`)

| Cenário | Descrição |
|---------|-----------|
| Fluxo completo | Endereço real → coordenadas → posição solar → diagnóstico |
| Fachada Norte | Verificar `has_sun = False` ou horas mínimas para fachada voltada ao norte no hemisfério sul |
| Solstício de verão vs inverno | Comparar `total_hours` entre as duas épocas para mesma localização |

### Ferramentas

- `pytest` para execução
- `pytest-cov` para cobertura (mínimo 80%)
- Mocks com `unittest.mock` para isolar chamadas externas (Nominatim, pvlib)
