# Real-time Air Quality Monitor

A GeoIT dashboard that pulls live Air Quality Index (AQI) data and renders it on an interactive Leaflet map. Flask backend, Dockerised for easy deployment.

---

## What it does

Fetches AQI readings from a public API, processes the data by location, and displays colour-coded air quality zones on a Leaflet map. Users can click any station marker to see PM2.5, PM10, CO, NO2, and overall AQI values.

---

## Stack

**Backend**
- Python, Flask
- `services/` layer for API integration and data processing
- `.env`-based config for API keys

**Frontend**
- Leaflet.js — interactive map with AQI overlays
- HTML/CSS/JavaScript

**Infrastructure**
- Docker + docker-compose for containerised deployment
- `.env.example` provided for environment setup

---

## Structure

```
Real-time-Air-Quality-Monitor/
├── app.py                  # Flask app entry point
├── config.py               # Config and env loading
├── services/               # API fetch and data processing layer
├── static/                 # CSS, JS
├── templates/              # HTML templates
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

---

## Running locally

```bash
git clone https://github.com/Alex-Mdau/Real-time-Air-Quality-Monitor
cd Real-time-Air-Quality-Monitor

# Copy and fill in your API key
cp .env.example .env

# Option 1: Run directly
pip install -r requirements.txt
python app.py

# Option 2: Run with Docker
docker-compose up --build
```

Open `http://localhost:5000`

---

## API

Uses a public AQI API (WAQI / OpenAQ compatible structure). Swap in your preferred provider via `.env`.

---

Built by [Alex Okumu](https://sites.google.com/view/okumugis) · Nairobi, Kenya
