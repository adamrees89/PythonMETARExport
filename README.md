# PythonMETARExport

A collection of scripts to fetch, parse, and export METAR (Meteorological Aerodrome Report) data as Prometheus metrics.

**Purpose:** provide a small, portable service that scrapes METAR data, performs calculations, and exposes metrics for Prometheus to scrape.

**What `metarGet.py` does**
- Connects to one or more METAR data sources (e.g. NOAA/AVWX or other APIs)
- Parses raw METAR strings into structured observations
- Performs basic calculations and normalisations (e.g., convert units, calculate derived fields)
- Exposes or writes metric values which will later be served via a Prometheus exporter endpoint

Current script is an early-stage prototype. It runs as a standalone script and prints or logs parsed results; the next steps are to turn it into a long-running service and expose metrics via the `prometheus_client` HTTP endpoint.

**Short-term goals**
- Polish and refactor `metarGet.py` so it can be imported as a library and run as a service
- Add unit and integration tests
- Add a minimal Prometheus exporter wrapper using `prometheus_client`
- Containerise the service with a small base image and provide a `docker-compose.yml` for local development

**Long-term goals**
- Support configurable station lists and schedules (cron-like polling)
- Add caching, rate-limiting and resilient retry/backoff for remote APIs
- Add observability (health checks, metrics for exporter internals)
- Publish to a package index or provide Helm charts for Kubernetes deployment

**Quickstart (local)**
Requirements: Python 3.11+ (recommended), see `requirements.txt`.

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the script (prototype):

```
python metarGet.py
```

**Quickstart (Docker)**
Build and run the container locally:

```
docker build -t python-metar-export .
docker run -p 8000:8000 python-metar-export
```

Or use `docker-compose`:

```
docker-compose up --build
```

Prometheus can then scrape metrics at `http://<host>:8000/metrics` once the exporter is added.

**To-Do**
- Polish `metarGet.py` (refactor into importable module and service entrypoint)
- Add unit and integration tests (pytest)
- Add `prometheus_client` exporter and HTTP server
- Create a small production-ready `Dockerfile` and `docker-compose.yml`
- Add CI checks (linting, tests)

**Suggested repository structure**

```
PythonMETARExport/
├─ metarGet.py            # main prototype script (entrypoint)
├─ README.md
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ CONTRIBUTING.md
├─ tests/
│  └─ test_general.py
└─ src/                  # future: refactored package code
	└─ pythonmetarexport/
		├─ __init__.py
		├─ collector.py
		├─ parser.py
		└─ exporter.py
```

**Contributing**
Please read `CONTRIBUTING.md` for guidelines on how to contribute, run tests, and open pull requests.

**License**
This project is public. See the `LICENSE` file for details.

--
If you'd like, I can also: add the initial `CONTRIBUTING.md`, a simple `tests/test_general.py`, a `Dockerfile`, `docker-compose.yml`, and a `requirements.txt` now.
