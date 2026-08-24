"""Simple Prometheus exporter that polls `metarGet.py` and exposes metrics.

This script depends on the prototype functions in `metarGet.py`:
- `Airports` dict
- `METARGet(airport_code)` -> raw JSON
- `PsychroCalc(METAROut)` -> dict of psychrometric values

Usage:
    python prometheus_exporter.py

Then visit http://localhost:8000/metrics
"""

import time
from prometheus_client import start_http_server, Gauge
from metarGet import Airports, METARGet, PsychroCalc


POLL_INTERVAL = 60


def make_gauges():
    gauges = {}
    for code in Airports.keys():
        lc = code.lower()
        gauges[f"dbtemp_{lc}"] = Gauge(f"metar_dbtemp_{lc}", f"Dry bulb temperature for {code}")
        gauges[f"dewpoint_{lc}"] = Gauge(f"metar_dewpoint_{lc}", f"Dew point for {code}")
        gauges[f"rhum_{lc}"] = Gauge(f"metar_rhum_{lc}", f"Relative humidity for {code}")
        gauges[f"up_{lc}"] = Gauge(f"metar_up_{lc}", f"Up status for {code}")
    return gauges


def run(poll_interval: int = POLL_INTERVAL):
    gauges = make_gauges()
    start_http_server(8000)
    while True:
        for code in Airports.keys():
            lc = code.lower()
            try:
                data = METARGet(code)
                air = PsychroCalc(data)
                gauges[f"dbtemp_{lc}"].set(air.get("DBTemp", float('nan')))
                gauges[f"dewpoint_{lc}"].set(air.get("DewPoint", float('nan')))
                gauges[f"rhum_{lc}"].set(air.get("RHum", float('nan')))
                gauges[f"up_{lc}"].set(1)
            except Exception:
                gauges[f"up_{lc}"].set(0)
        time.sleep(poll_interval)


if __name__ == "__main__":
    run()
