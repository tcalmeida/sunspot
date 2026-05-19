# Requirements Document

## Introduction

Este documento especifica as dependências de software necessárias para desenvolver e executar o MVP Sunspot. O projeto é uma aplicação web em Python/Streamlit que traduz dados astronômicos de trajetória solar em diagnósticos práticos para inquilinos avaliando a incidência de luz solar em imóveis.

## Requirements

### Core Dependencies

#### Streamlit
- **Versão:** 1.28.0+
- **Propósito:** Framework web para construir a interface interativa da aplicação
- **Uso:** Criar UI responsiva, campos de entrada, exibição de resultados e loading states
- **Instalação:** `pip install streamlit`

#### geopy
- **Versão:** 2.3.0+
- **Propósito:** Geolocalização e geocodificação de endereços
- **Uso:** Converter endereço em coordenadas (latitude, longitude) usando Nominatim
- **Instalação:** `pip install geopy`

#### pvlib
- **Versão:** 0.10.0+
- **Propósito:** Cálculos de posição solar e trajetória astronômica
- **Uso:** Calcular azimute, elevação e posição do sol ao longo do dia
- **Instalação:** `pip install pvlib`

#### pandas
- **Versão:** 2.0.0+
- **Propósito:** Manipulação e análise de dados tabulares
- **Uso:** Processar séries temporais de posição solar, filtros e agregações
- **Instalação:** `pip install pandas`

### Development Dependencies

#### ruff
- **Versão:** 0.1.0+
- **Propósito:** Linter rápido para Python
- **Uso:** Verificar qualidade de código e conformidade com padrões
- **Instalação:** `pip install ruff`

#### black
- **Versão:** 23.0.0+
- **Propósito:** Formatador de código Python
- **Uso:** Garantir formatação consistente do código
- **Instalação:** `pip install black`

#### mypy
- **Versão:** 1.5.0+
- **Propósito:** Type checker estático para Python
- **Uso:** Validar tipagem em modo strict
- **Instalação:** `pip install mypy`

### Optional Dependencies

#### pytz
- **Versão:** 2023.3+
- **Propósito:** Manipulação de timezones
- **Uso:** Garantir cálculos corretos com timezone-aware datetime
- **Instalação:** `pip install pytz`

#### python-dotenv
- **Versão:** 1.0.0+
- **Propósito:** Carregamento de variáveis de ambiente
- **Uso:** Gerenciar configurações sensíveis (user_agent do geopy, etc.)
- **Instalação:** `pip install python-dotenv`

## Glossary

| Termo | Definição |
|-------|-----------|
| **Azimute** | Ângulo horizontal medido em graus (0° a 360°) que indica a direção do sol em relação ao norte |
| **Elevação Solar** | Ângulo vertical do sol acima do horizonte (0° a 90°) |
| **Geocodificação** | Processo de converter um endereço em coordenadas geográficas (latitude, longitude) |
| **Timezone-aware** | Datetime que inclui informação de fuso horário |
| **Nominatim** | Serviço de geocodificação aberto baseado em dados OpenStreetMap |
| **pvlib** | Biblioteca Python para cálculos de posição solar e radiação |
| **Streamlit** | Framework Python para criar aplicações web interativas sem necessidade de JavaScript/HTML/CSS |

## Installation Instructions

### 1. Criar ambiente virtual (recomendado)

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## Compatibility

- **Python:** 3.11+
- **Sistemas Operacionais:** Linux, macOS, Windows
- **Navegadores:** Chrome, Firefox, Safari, Edge (para Streamlit)

## Notes

- Todas as versões são pinadas para garantir reprodutibilidade
- As dependências foram selecionadas por serem mantidas ativamente e amplamente utilizadas
- O arquivo `requirements.txt` contém todas as dependências: runtime e ferramentas de qualidade de código
