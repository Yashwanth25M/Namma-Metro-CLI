# Namma Metro CLI

Lightweight command-line **route estimator** for the Bangalore *Namma Metro* network.

> Type origin and destination station names (supports fuzzy matching / typos) and get an estimated route, total distance and arrival time using live GeoJSON station data.

---

## Snapshot (what this code does)

- Downloads a public GeoJSON of metro stations (default URL: `https://raw.githubusercontent.com/geohacker/namma-metro/master/metro-lines-stations.geojson`).
- Builds a spatial graph connecting each station to its nearest neighbors on the same line.
- Uses Dijkstra (priority queue) on travel-time edge weights (ride time + dwell time) to estimate fastest route.
- CLI supports fuzzy/substring search for stations (uses Python `difflib`), prints colorized step-by-step route and ETA.

---

## Quick start

```bash
# Clone and run 
git clone https://github.com/Yashwanth25M/namma-metro-cli
cd namma-metro-cli
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.\.venv\Scripts\activate  # Windows (PowerShell/CMD)
pip install -r requirements.txt
python namma_metro_cli.py
```

When prompted, type the origin and destination station names. The CLI will try exact/substring matches first and fall back to fuzzy suggestions.

Example run (user input shown):

```
Origin Station: MG Road
Destination Station: Majestic

Route Found:
  1. MG Road [Purple Line]
  2. Trinity [Purple Line]
  3. Cubbon Park [Purple Line]
  4. Vidhana Soudha [Purple Line]
  5. Majestic [Multiple Lines]

Summary:
  Total Distance: 5.80 km
  Est. Time:      12 min 20 sec
  Arrival:        14:18:33
```

---

## Configuration (constants in code)

- `GEOJSON_URL` — default GeoJSON URL for stations.
- `AVG_SPEED_KMH` (float) — commercial running speed assumed for ride time (default `35.0` km/h).
- `DWELL_SEC` (int) — fixed dwell time at each stop (default `30` seconds).
- `NEAREST_NEIGH` (int) — number of nearest neighbors per station to connect on the same metro line (default `4`).

Tweak these constants to change route-time behaviour.

---

## Implementation details

### Data parsing
- The GeoJSON `features` are parsed robustly: the script looks for station names in several possible property keys (`name`, `station_name`, `stop_name`, `title`).
- Line information is parsed from `line`, `lines`, `route` or `color` properties. If none found, the station is assigned to a default `Metro` group.
- Station IDs are normalized by lowercasing and stripping `" station"` suffix for stable internal keys.

### Graph construction
- For each line group, the script computes pairwise haversine distances (using `haversine_km`) between stations.
- Each station connects to its `NEAREST_NEIGH` nearest stations on the same line. Each edge stores three things: `(neighbor_id, edge_cost_seconds, distance_km)`.
- Edge cost = travel time in seconds (`distance / AVG_SPEED_KMH * 3600`) + `DWELL_SEC`.

### Routing
- Dijkstra's algorithm (min-heap via `heapq`) finds the time-optimal path from origin to destination.
- The algorithm returns the path (list of station ids) and total travel time in seconds.

### Fuzzy search UI
- Station lookup uses:
  1. Case-insensitive substring matching of `display_name`.
  2. If no substring match, `difflib.get_close_matches()` to suggest top 3 close names (cutoff=0.5).
- If multiple matches exist, the user is prompted to select the correct station.

---

## Dependencies

- `requests` — for fetching GeoJSON.
- `colorama` — ANSI terminal color output.

## Known limitations & suggestions

- **Line connectivity assumption**: the script connects stations by nearest geographic distance within a line group. This may incorrectly link non-adjacent stations if the line order in the GeoJSON is not sequential. For greater accuracy, prefer connecting using the order provided in the GeoJSON (if available) or by parsing explicit adjacency.
- **NEAREST_NEIGH tradeoff**: higher `NEAREST_NEIGH` yields more connectivity (can find alternate paths) but increases false transfers across long lines.
- **No transfer penalty**: transfers between lines at interchange stations are not explicitly penalized (only dwell time is used). Consider adding a transfer penalty constant if you want to model transfer times.
- **Station naming / aliasing**: multiple display names or common aliases are not mapped. A small alias map can improve UX (e.g., `Majestic` / `KSR Bengaluru` aliases).
- **No caching**: GeoJSON is fetched every run. Implement a simple file cache to avoid repeated network calls.
- **No unit tests**: Add tests for `haversine_km`, `build_network`, `build_graph`, and `dijkstra`.

---
