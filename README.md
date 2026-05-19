# ☀️ Sunspot

Web app que traduz a trajetória solar em diagnósticos práticos para quem está avaliando a incidência de luz solar em um imóvel.

Informe o endereço, o ângulo da janela principal e a época do ano — a aplicação retorna os horários de sol direto, o total de horas e recomendações sobre o imóvel.

---

## Requisitos

- Python 3.10
- pip

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd sunspot

# 2. Crie o ambiente virtual
python3.10 -m venv .venv
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env e ajuste NOMINATIM_USER_AGENT
```

---

## Uso

```bash
# Acesso local
.venv/bin/streamlit run app.py

# Acesso na rede local (outros devices)
.venv/bin/streamlit run app.py --server.address 0.0.0.0
```

Acesse em `http://localhost:8501` ou `http://<seu-ip>:8501`.

---

## Como usar a aplicação

1. **Endereço** — informe o endereço completo do imóvel
2. **Ângulo da janela (azimute)** — direção para a qual a janela está voltada, em graus a partir do Norte (use a bússola do celular)
   - 0° → Norte · 90° → Leste · 180° → Sul · 270° → Oeste
3. **Época do ano** — Verão ou Inverno
4. Clique em **Calcular Incidência Solar**

---

## Variáveis de ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `NOMINATIM_USER_AGENT` | Identificador enviado ao serviço de geocodificação | `sunspot-mvp` |

---

## Estrutura do projeto

```
sunspot/
├── app.py                  # Entry point
├── requirements.txt
├── pyproject.toml
├── .env.example
└── app/
    ├── config/settings.py  # Constantes e configurações
    ├── domain/diagnostics.py # Regras de negócio
    ├── services/
    │   ├── geolocation.py  # Geocodificação (geopy/Nominatim)
    │   └── solar.py        # Posição solar (pvlib)
    ├── ui/main_page.py     # Interface Streamlit
    └── utils/
        ├── angle.py        # Cálculo angular
        └── exceptions.py   # Hierarquia de exceções
```

---

## Qualidade de código

```bash
ruff check .
black --check .
mypy .
```

---

## Stack

| Biblioteca | Uso |
|---|---|
| [Streamlit](https://streamlit.io) | Interface web |
| [pvlib](https://pvlib-python.readthedocs.io) | Cálculo de posição solar |
| [geopy](https://geopy.readthedocs.io) | Geocodificação de endereços |
| [pandas](https://pandas.pydata.org) | Processamento de séries temporais |
