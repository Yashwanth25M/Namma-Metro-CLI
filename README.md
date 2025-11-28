# Namma Metro CLI


![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Requests](https://img.shields.io/badge/Requests-API%20Calls-green)
![Colorama](https://img.shields.io/badge/Colorama-CLI%20Colors-yellow)
![Dijkstra](https://img.shields.io/badge/Algorithm-Dijkstra-red)

A small **Python 3** command-line tool to plan fastest routes across Bengaluru’s **Namma Metro** network.  
It builds a graph from station metadata, computes fastest routes (Dijkstra), offers interactive fuzzy station search, browsable lines, and human-friendly route summaries (distance, stops, interchanges, estimated travel time).

---



## Table of Contents

1. Features  
2. Example CLI Output  
3. Installation  
4. Configuration  
5. Usage  
6. How it works (internals)  
7. Customization & Extensibility  
8. Limitations & Future Improvements  
9. Contributing  
10. License  
11. Acknowledgements

---

## Features

- Fastest route calculation using **Dijkstra’s algorithm**
- Interactive **fuzzy search**
- Browse stations **by line**
- Supports explicit line ordering via `line_sequences.json`
- Distance, stops, interchanges & travel time estimation
- Repeat last route, reverse route
- Colored CLI output (`colorama`)

---

## Example CLI Output

```
==========================
   Namma Metro CLI
   Type 'q' anytime to quit
==========================
1. Plan a route
2. Browse stations by line
3. Repeat last route
0. Exit
```

### Route example
```
Route found:
1. Jalahalli [Green]
2. Peenya [Green]
3. Dasarahalli [Green]
4. Nagasandra [Green]

Summary (12:42):
Stops: 3
Interchanges: 0
Distance: 6.8 km
Estimated in-train time: 11m 40s
```

---

## Installation

### Requirements
- Python 3.7+
- `colorama`

### Steps
```bash
pip install colorama
```

or

```bash
pip install -r requirements.txt
```

---

## Configuration

### `stations.json` (required)
Example:
```json
[
  {
    "id": "jalahalli",
    "name": "Jalahalli",
    "lat": 13.0225,
    "lon": 77.5423,
    "lines": ["Green"]
  }
]
```

### `line_sequences.json` (optional)
```json
{
  "Green": ["jalahalli", "peenya", "dasarahalli", "nagasandra"]
}
```

---

## Usage

Run:
```bash
python main.py
```

Menu:
- Plan route
- Browse stations
- Repeat last route
- Exit

---

## How It Works (Internals)

- Builds graph using **haversine** distance + dwell time  
- Computes time = distance/AVG_SPEED + DWELL_SEC  
- Dijkstra finds minimum-time path  
- Fuzzy search via substring + `difflib.get_close_matches`  
- Interchanges counted by stations belonging to >1 line  

---

## Customization

Modify constants:
- `AVG_SPEED_KMH`
- `DWELL_SEC`

Extend JSON files to add more stations/lines.

---

## Limitations & Future Improvements

- Constant speed (no real timetable)
- No live frequency / real-time data
- No transfer walking times
- Future: real schedules, GUI, API backend

---
