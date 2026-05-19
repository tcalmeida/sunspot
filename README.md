# ☀️ Sunspot

Web app that translates solar trajectory data into practical diagnostics for anyone evaluating sunlight exposure in a property.

Enter the address, the main window angle, and the season — the app returns the direct sunlight hours, total duration, and practical recommendations about the property.

---

## Requirements

- Python 3.10
- pip

---

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd sunspot

# 2. Create the virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set NOMINATIM_USER_AGENT
```

---

## Usage

```bash
# Local access
.venv/bin/streamlit run app.py

# Local network access (other devices)
.venv/bin/streamlit run app.py --server.address 0.0.0.0
```

Access at `http://localhost:8501` or `http://<your-ip>:8501`.

---

## How to use

1. **Address** — enter the full property address
2. **Window angle (azimuth)** — the direction the main window faces, in degrees from North (use your phone's compass)
   - 0° → North · 90° → East · 180° → South · 270° → West
3. **Season** — Summer or Winter
4. Click **Calculate Sun Exposure**

The app automatically detects the hemisphere from the geocoded latitude and uses the correct solstice date for the selected season.

---

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `NOMINATIM_USER_AGENT` | Identifier sent to the geocoding service | `sunspot-mvp` |

---

## Project structure

```
sunspot/
├── app.py                    # Entry point
├── requirements.txt
├── pyproject.toml
├── .env.example
└── app/
    ├── config/settings.py    # Constants and configuration
    ├── domain/diagnostics.py # Business rules
    ├── services/
    │   ├── geolocation.py    # Geocoding (geopy/Nominatim)
    │   └── solar.py          # Solar position (pvlib)
    ├── ui/
    │   ├── main_page.py      # Streamlit interface
    │   └── i18n.py           # UI translations (PT / EN)
    └── utils/
        ├── angle.py          # Angular calculation helpers
        ├── season.py         # Hemisphere-aware solstice resolution
        └── exceptions.py     # Exception hierarchy
```

---

## Code quality

```bash
ruff check .
black --check .
mypy .
```

---

## Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web interface |
| [pvlib](https://pvlib-python.readthedocs.io) | Solar position calculation |
| [geopy](https://geopy.readthedocs.io) | Address geocoding |
| [pandas](https://pandas.pydata.org) | Time series processing |
