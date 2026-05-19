# Implementation Plan

## Overview

MVP da aplicação Sunspot: web app em Python/Streamlit que traduz dados astronômicos de trajetória solar em diagnósticos práticos para inquilinos avaliando a incidência de luz solar em imóveis. A arquitetura é modular e desacoplada em cinco camadas: config, utils, domain, services e ui.

## Tasks

- [x] 1. Criar estrutura de pastas do projeto: `app/ui/`, `app/services/`, `app/domain/`, `app/utils/`, `app/config/`, com todos os arquivos `__init__.py` em cada módulo
- [x] 2. Criar `app.py` como entry point mínimo do Streamlit (título e layout inicial) e verificar que `streamlit run app.py` executa sem erros
- [x] 3. Criar `pyproject.toml` com configuração de `ruff`, `black` e `mypy --strict`, e `.env.example` com as variáveis de ambiente esperadas
- [x] 4. Implementar `app/config/settings.py` com todas as constantes: `APP_NAME`, `NOMINATIM_USER_AGENT`, `GEOCODING_TIMEOUT_SECONDS`, `SOLAR_INTERVAL_MINUTES`, `MIN_SOLAR_ELEVATION_DEGREES`, `ANGULAR_TOLERANCE_DEGREES`, `SUMMER_SOLSTICE` e `WINTER_SOLSTICE`; carregar `NOMINATIM_USER_AGENT` via variável de ambiente com fallback
- [x] 5. Implementar `app/utils/exceptions.py` com a hierarquia de exceções: `SunspotError`, `GeocodingError(SunspotError)` e `SolarCalculationError(SunspotError)`
- [x] 6. Implementar `app/utils/angle.py` com `angular_difference(a: float, b: float) -> float` que retorna a diferença mínima entre dois ângulos com wrap-around correto (resultado sempre em `[0°, 180°]`)~
- [x] 7. Implementar `app/services/geolocation.py` com dataclass `GeoLocation` e função `geocode_address(address: str) -> GeoLocation` usando `geopy.geocoders.Nominatim`; tratar timeout, endereço não encontrado e erros de serviço lançando `GeocodingError`; adicionar logging para falhas
- [x] 8. Implementar `app/services/solar.py` com dataclass `SolarData` e função `calculate_solar_position(latitude, longitude, date, interval_minutes) -> SolarData` usando `pvlib.solarposition.get_solarposition` e `pandas.date_range` com timezone-aware; tratar erros lançando `SolarCalculationError`
- [x] 9. Implementar `app/domain/diagnostics.py` com enum `FacadeOrientation` (8 octantes), dataclass `SunExposureResult`, e as funções `classify_orientation`, `generate_recommendations` e `calculate_sun_exposure`; aplicar os três filtros de interseção solar (noturno, horizonte e angular); garantir que nenhum import de `streamlit`, `geopy` ou `pvlib` existe neste módulo
- [x] 10. Implementar `app/ui/main_page.py` com as funções `render_inputs`, `render_results`, `render_error` e `render_main_page`; orquestrar o fluxo completo com `st.spinner`, validação de inputs e tratamento de erros amigável
- [x] 11. Finalizar `app.py` com `st.set_page_config` e chamada a `render_main_page()`; executar `ruff check .`, `black --check .` e `mypy .` sem erros

## Task Dependency Graph

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": ["1", "2", "3"]
    },
    {
      "wave": 2,
      "tasks": ["4", "5"]
    },
    {
      "wave": 3,
      "tasks": ["6"]
    },
    {
      "wave": 4,
      "tasks": ["7", "8"]
    },
    {
      "wave": 5,
      "tasks": ["9"]
    },
    {
      "wave": 6,
      "tasks": ["10"]
    },
    {
      "wave": 7,
      "tasks": ["11"]
    }
  ]
}
```

## Notes

- Tasks 1, 2 e 3 podem ser feitas em paralelo — são independentes entre si.
- Tasks 4 e 5 podem ser feitas em paralelo — ambas dependem apenas da estrutura criada na wave 1.
- Tasks 7 e 8 podem ser feitas em paralelo — ambas dependem de config (4) e exceptions (5).
- Task 9 (domínio) depende de Task 6 (utils/angle) e Task 8 (SolarData), mas não deve importar pvlib diretamente.
- Task 10 (UI) só deve ser iniciada após Task 9 estar completa e validada.
- **Testes são gerados somente após a aplicação estar funcionando, mediante solicitação explícita do usuário.**
