# Namma Metro CLI

> Lightweight command-line route estimator for the Bangalore Namma Metro network.

**Quick**: type origin and destination station names (supports typos / fuzzy match) and get an estimated route, distance and arrival time using live GeoJSON station data.

---

## Features

- Fetches station locations from a public GeoJSON on GitHub.
- Fuzzy search for station names (handles typos and partial matches).
- Builds a nearest-neighbour graph per metro line and estimates travel time using haversine distance + simple speed/dwell model.
- Shows step-by-step route, total distance, ETA and trip duration.
- Minimal dependencies and easy to run from the terminal.

---

## Requirements

- Python 3.8+
- Packages (install via pip):
  - `requests`
  - `colorama`

Install dependencies:

```bash
pip install -r requirements.txt
# OR
pip install requests colorama
