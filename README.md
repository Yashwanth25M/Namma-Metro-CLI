# Namma Metro CLI Route Planner  
**(Fully Updated for 2025 – includes latest Namma Metro station data structure support)**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Colorama](https://img.shields.io/badge/CLI-Colorama-yellow)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra-red)
![Updated](https://img.shields.io/badge/Data%20Status-Updated%20for%202025-brightgreen)

A **Python 3** command-line tool to plan the fastest routes across Bengaluru’s **Namma Metro** network.  
This project is **fully updated for 2025**, supporting the current network structure, expandable station data,  
and flexible line sequences for future metro extensions.

It loads station metadata from JSON, builds a weighted graph of the network, uses **Dijkstra’s algorithm**  
to compute the fastest route, and displays a clean, human-friendly summary with distance, stops,  
interchanges, and estimated travel time.

---

## Table of Contents

1. [Features](#features)  
2. [Example CLI Output](#example-cli-output)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
   - [`stations.json` (required)](#stationsjson-required)  
   - [`line_sequences.json` (optional)](#line_sequencesjson-optional)  
5. [Usage](#usage)  
6. [How It Works (Internals)](#how-it-works-internals)  
7. [Customization & Extensibility](#customization--extensibility)  
8. [Limitations & Future Improvements](#limitations--future-improvements)  
9. [Contributing](#contributing)  
10. [License](#license)  
11. [Acknowledgements](#acknowledgements)

---

## Features

- 🚇 **Route planning with Dijkstra**  
  Computes the **fastest route** between any two stations using Dijkstra’s algorithm on a weighted graph.

- 🔍 **Fuzzy station search**  
  Type any part of the station name; if needed, fuzzy matching (`difflib`) suggests close matches.

- 🧵 **Stations by line**  
  Browse all stations grouped by line (e.g. Green, Purple).

- 📏 **Distance & time estimation**  
  Uses the **haversine formula** for distance and assumes a configurable **average speed** and **dwell time** to estimate in-train travel time.

- 🔁 **Repeat & reverse routes**  
  Quickly re-run your last planned route or reverse it (destination ⇄ origin) with one keystroke.

- 🎨 **Colored CLI output**  
  Uses `colorama` to improve readability in the terminal (highlights for menus, errors, and summaries).

---

## Example CLI Output

### Main menu

```text
==========================
   Namma Metro CLI
   Type 'q' anytime to quit
==========================
1. Plan a route
2. Browse stations by line
3. Repeat last route
0. Exit
Choose an option: 1
```

### Planning a route (with fuzzy search)

```text
Tip: you can type any part of the station name. Fuzzy suggestions will be shown.

Origin station: jalah
Matches:
  1) Jalahalli [Green]
Choose number (or Enter to search again): 1
Selected: Jalahalli

Destination station: nagasan
Matches:
  1) Nagasandra [Green]
Choose number (or Enter to search again): 1
Selected: Nagasandra
```

### Route result

```text
Route found:

 1. Jalahalli [Green]
 2. Peenya [Green]
 3. Dasarahalli [Green]
 4. Nagasandra [Green]

Summary (12:42)
---------------
Origin: Jalahalli
Destination: Nagasandra
Total stops: 3
Interchanges: 0
Total distance: 6.8 km
Estimated in-train time: 11m 40s

Note: Time is an estimate based only on distance, average speed, and dwell time. No real timetable data is used.

[R]everse route   [N]ew route   [M]ain menu
Choice:
```

---

## Installation

### Requirements

- **Python**: 3.8+  
- **Dependencies**:
  - Standard library: `math`, `sys`, `heapq`, `json`, `difflib`, `datetime`, `collections`
  - External: `colorama`

### Setup

1. **Clone or download** this repository into a folder of your choice.
2. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv .venv
   # Linux / macOS
   source .venv/bin/activate
   # Windows
   .venv\Scriptsctivate
   ```

3. **Install dependencies**:

   ```bash
   pip install colorama
   ```

   Or, if a `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The CLI expects its data in JSON files:

- `stations.json` (required) — describes all metro stations.
- `line_sequences.json` (optional) — defines the explicit order of stations on each line.

By default, the script looks for these files in the **current working directory**.

### `stations.json` (required)

This file is a JSON array of station objects.  
Each station must have:

- `id` — a unique string identifier  
- `name` — display name (string)  
- `lat` — latitude (float)  
- `lon` — longitude (float)  
- `lines` — array of line names this station belongs to

**Example:**

```json
[
  {
    "id": "jalahalli",
    "name": "Jalahalli",
    "lat": 13.0225,
    "lon": 77.5423,
    "lines": ["Green"]
  },
  {
    "id": "peenya",
    "name": "Peenya",
    "lat": 13.0160,
    "lon": 77.5478,
    "lines": ["Green"]
  },
  {
    "id": "nagasandra",
    "name": "Nagasandra",
    "lat": 13.0426,
    "lon": 77.5145,
    "lines": ["Green"]
  }
]
```

On load, the script builds:

- `stations`: a dictionary mapping station ID → station metadata
- `line_groups`: a mapping of line name → list of station IDs on that line

### `line_sequences.json` (optional)

This file specifies the **exact ordering** of stations on each line.  
If a line is missing from this file, the script falls back to the order in `line_groups` derived from `stations.json`.

**Example:**

```json
{
  "Green": [
    "jalahalli",
    "peenya",
    "dasarahalli",
    "nagasandra"
  ],
  "Purple": [
    "kengeri",
    "mysore_road",
    "vijayanagar",
    "magadi_road"
  ]
}
```

---

## Usage

Make sure `stations.json` (and optionally `line_sequences.json`) are present in the same folder as the script, then run:

```bash
python main.py
```


### Main Menu Flow

Once started, you’ll see a menu like:

```text
1. Plan a route
2. Browse stations by line
3. Repeat last route        # Only shown after you have planned at least one route
0. Exit
```

#### 1. Plan a route

- Prompts you for an **origin** and **destination** station.
- You can type any substring of the station name (e.g., `jalah`, `mej`, `bai`).
- If no direct substring match is found, the program suggests fuzzy matches based on `difflib.get_close_matches`.
- After both stations are selected, the tool:
  - Computes the **fastest route** using Dijkstra.
  - Prints the ordered station list.
  - Displays a summary with:
    - Total stops
    - Interchanges
    - Total distance
    - Estimated in-train time

#### 2. Browse stations by line

- Displays all available metro lines.
- You choose a line by number.
- Prints all station names on that line in order (using `line_sequences.json` if available).

#### 3. Repeat last route

- Available only if you have successfully planned a route before.
- Reuses the last origin/destination pair and recalculates the route.
- Very handy when exploring reverse or alternate trips.

#### 0 / `q` / `quit` / `exit`

- Cleanly exits the application.

### After Route Options

After a route summary is shown, you’ll be offered:

- `[R]everse route` — swap origin and destination and recompute.
- `[N]ew route` — choose a new origin and destination.
- `[M]ain menu` — return to the main menu.

---

## How It Works (Internals)

### Data Loading

- `load_stations_from_file(filename)`  
  - Loads `stations.json`.
  - Populates:
    - `stations` (dict): `{station_id: {id, name, lat, lon, lines}}`
    - `line_groups` (dict): `{line_name: [station_id, ...]}`

- `load_line_sequences(filename)`  
  - Attempts to load `line_sequences.json`.
  - On failure (file missing/invalid), logs an error and returns `{}`.

### Distance Calculation

- `haversine_km(lat1, lon1, lat2, lon2)`  
  - Uses the **haversine formula** to compute great-circle distance between two latitude/longitude pairs.
  - Returns distance in **kilometers**.

### Graph Construction

- `build_graph(stations, line_groups, line_sequences)`:
  - Iterates over each metro line.
  - For each line, determines station order:
    - Use `line_sequences[line_name]` if available.
    - Otherwise, use `line_groups[line_name]`.
  - For every consecutive pair of stations `(A, B)`:
    - Compute distance `d_km` via `haversine_km`.
    - Compute ride time: `ride_time_sec = d_km / AVG_SPEED_KMH * 3600`.
    - Add dwell time: `edge_cost_sec = ride_time_sec + DWELL_SEC`.
    - Add **undirected** edges:
      - `A → B` with `(neighbor_id, edge_cost_sec, d_km)`
      - `B → A` with the same cost and distance.

### Pathfinding

- `dijkstra(adj, start_id, goal_id)`:
  - Standard **Dijkstra’s algorithm** using a priority queue (`heapq`).
  - Items in the heap: `(total_cost_so_far, station_id, path_so_far)`.
  - Keeps track of the best known time to each station.
  - Returns:
    - `path` — list of station IDs from origin to destination.
    - `cost` — total travel time in seconds.

### Station Selection & Fuzzy Search

- `get_user_selection(stations, prompt_text)`:
  - Prompts for user input (station search term).
  - Finds stations whose names contain the substring (case-insensitive).
  - If none are found:
    - Uses `difflib.get_close_matches` to suggest likely candidates.
  - Handles:
    - Single match → automatically selects it.
    - Multiple matches → list numbered options and lets user choose.
    - `q` / `quit` / `exit` → cancels and returns to caller.

### Interchanges

- `compute_interchanges(path, stations)`:
  - Examines intermediate stations (excluding origin and destination).
  - Counts how many have `len(station["lines"]) > 1`.
  - This count is displayed as the number of **interchanges** in the summary.

---

## Customization & Extensibility

### Timing Model

At the top of the script, you’ll typically see:

```python
AVG_SPEED_KMH = 35.0  # Average in-train speed
DWELL_SEC = 30        # Per-station dwell time in seconds
```

You can modify:

- `AVG_SPEED_KMH` — if you want to assume faster/slower trains.
- `DWELL_SEC` — to represent longer or shorter stops at stations.

### Network Data

- To **add new stations**, append them to `stations.json` with correct latitude/longitude and line membership.
- To adjust line ordering or add new lines, edit `line_sequences.json` accordingly.

### Possible Extensions

- Export the route as JSON or CSV.
- Wrap the CLI in a simple **web API** (e.g., FastAPI/Flask).
- Add a **TUI** (text-based UI) front-end using libraries like `rich` or `textual`.
- Build a **GUI** in PyQt, Tkinter, or a web frontend that calls this CLI logic.

---

## Limitations & Future Improvements

### Current Limitations

- Assumes a **constant average speed** (no congestion, no varying acceleration).
- Uses a **fixed dwell time** for all stations.
- Does **not** include real timetable, frequency, or live operation data.
- Transfers (interchanges) do not include walking time inside stations.
- The accuracy of the map depends entirely on the quality of the JSON data.

### Potential Future Improvements

- Integrate real-time or scheduled data (if available) for more accurate timings.
- Model **platform-to-platform transfer times**.
- Support **alternative route suggestions** (e.g., next-best path).
- Add unit tests and continuous integration.
- Package it as a `pip`-installable module.

---

## Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Make and commit your changes: `git commit -m "Add my feature"`.
4. Push to your fork and open a Pull Request.

Please:

- Keep PRs focused on a single change/feature.
- Update documentation (including this README) when behavior changes.
- If you modify network data, mention the source and reasoning.

---

## License

This project is released under the **MIT License**.  
See the `LICENSE` file in this repository for full text.

---

## Acknowledgements

- **Namma Metro (BMRCL)** — for the real-world system that inspired this tool.
- **Python community** — for a rich standard library and ecosystem.
- **Colorama** — for making cross-platform colored CLI output easy.
- Everyone who contributes station data, bug reports, and improvements.
