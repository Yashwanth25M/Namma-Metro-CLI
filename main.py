import math, sys, heapq, difflib, json
from collections import defaultdict
from colorama import init, Fore, Style
from datetime import datetime, timedelta

init(autoreset=True)

STATIONS_FILE = "stations.json"
LINE_SEQ_FILE = "line_sequences.json"
AVG_SPEED_KMH = 35.0
DWELL_SEC = 30

def load_stations_from_file(filename):
    """Load station metadata from JSON and group them by line."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw_stations = json.load(f)
    except Exception as e:
        print(Fore.RED + f"Error loading stations file: {e}")
        sys.exit(1)

    stations = {}
    line_groups = defaultdict(list)

    for item in raw_stations:
        sid = item["id"]
        stations[sid] = {
            "id": sid,
            "display_name": item["name"],
            "lat": item["lat"],
            "lon": item["lon"],
            "lines": set(item["lines"]),
        }
        for line in item["lines"]:
            line_groups[line].append(sid)

    return stations, line_groups

def load_line_sequences(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        quit
        print(Fore.RED + f"Error loading line sequences: {e}")
        return {}
    
def build_graph(stations, line_groups, line_sequences):
    """
    Build a graph where edges connect consecutive stations on each line.

    - For lines listed in line_sequences, we use that explicit order.
    - For other lines, we just use the JSON order.
    """
    adj = defaultdict(list)

    for line, sids in line_groups.items():
        if line in line_sequences:
            ordered = [sid for sid in line_sequences[line] if sid in sids]
        else:
            ordered = sids[:]

        if len(ordered) < 2:
            continue

        for i in range(len(ordered) - 1):
            a_id = ordered[i]
            b_id = ordered[i + 1]

            a = stations[a_id]
            b = stations[b_id]

            d_km = haversine_km(a["lat"], a["lon"], b["lat"], b["lon"])
            ride_sec = (d_km / AVG_SPEED_KMH) * 3600
            total_cost = ride_sec + DWELL_SEC

            adj[a_id].append((b_id, total_cost, d_km))
            adj[b_id].append((a_id, total_cost, d_km))

    return adj

def list_stations_menu(stations, line_groups):
    """Interactive menu to browse stations line-wise."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🗺  Browse Stations by Line")
    lines = sorted(line_groups.keys())
    for i, line in enumerate(lines, 1):
        print(f"  {i}. {line}")
    print("  0. Back to main menu")

    choice = input("\nSelect a line number: ").strip()
    if not choice.isdigit():
        return
    idx = int(choice)
    if idx == 0 or not (1 <= idx <= len(lines)):
        return

    line = lines[idx - 1]
    if idx == 1:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Stations on {line} Line:\n")
    elif idx == 2:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Stations on {line} Line:\n")
    elif idx == 3:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Stations on {line} Line:\n")

    for sid in line_groups[line]:
        s = stations[sid]
        print(f"  • {s['display_name']}")
    print()

def get_user_selection(stations, prompt_text):
    """Interactive fuzzy search to select a station from user input."""
    all_names = [s["display_name"] for s in stations.values()]
    name_to_id = {s["display_name"]: s["id"] for s in stations.values()}

    while True:
        query = input(f"{prompt_text} (or 'q' to cancel): ").strip()
        if not query or query.lower() in ("q", "quit", "exit"):
            return None

        matches = [
            s
            for s in stations.values()
            if query.lower() in s["display_name"].lower()
        ]

        if not matches:
            guesses = difflib.get_close_matches(query, all_names, n=3, cutoff=0.5)
            if guesses:
                print(f"{Fore.YELLOW}No exact match found. Did you mean...?")
                matches = [stations[name_to_id[g]] for g in guesses]
            else:
                print(f"{Fore.RED}No matches found. Check spelling.")
                continue

        if len(matches) == 1:
            print(f"{Fore.CYAN}Selected: {matches[0]['display_name']}")
            return matches[0]["id"]

        print(f"{Fore.CYAN}Multiple matches found:")
        for i, m in enumerate(matches[:10], 1):
            lines = ", ".join(m["lines"])
            print(f" {i}. {m['display_name']} ({lines})")

        sel = input("Select number (or Enter to search again): ")
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(matches):
                return matches[idx]["id"]

def dijkstra(adj, start_id, goal_id):
    """Compute shortest-time path between two stations using Dijkstra's algorithm."""
    pq = [(0, start_id, [])]

    visited = set()
    min_times = {start_id: 0}

    while pq:
        cost, cur, path = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)
        path = path + [cur]
        if cur == goal_id:
            return path, cost

        for neighbor, edge_cost, _ in adj[cur]:
            new_cost = cost + edge_cost
            if new_cost < min_times.get(neighbor, float("inf")):
                min_times[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path))
    return None, 0
            
def haversine_km(lat1, lon1, lat2, lon2):
    """Return great-circle distance between two lat/lon points in km."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def compute_interchanges(path, stations):
    """Count intermediate stations that belong to multiple lines."""
    interchanges = 0
    for i, sid in enumerate(path):
        if i == 0 or i == len(path) - 1:
            continue
        if len(stations[sid]["lines"]) > 1:
            interchanges += 1
    return interchanges

def fmt_time(dt):
    """Format datetime as HH:MM."""
    return dt.strftime("%H:%M")


def main():
    """CLI entry point for the Namma Metro route planner."""
    print(f"{Fore.GREEN}{Style.BRIGHT}=== Namma Metro CLI ===")
    print(f"{Fore.YELLOW}Type 'q' anytime to quit.\n")

    stations, line_groups = load_stations_from_file(STATIONS_FILE)
    print(f"{Fore.BLUE}Loaded {len(stations)} stations.")

    line_sequences = load_line_sequences(LINE_SEQ_FILE)
    adj = build_graph(stations, line_groups, line_sequences)

    last_origin = None
    last_destination = None

    while True:
        print("\n" + "-" * 40)
        print(f"{Fore.CYAN}{Style.BRIGHT}Main Menu")
        print("  1. Plan a route")
        print("  2. Browse stations by line")
        if last_origin and last_destination:
            print("  3. Repeat last route")
        print("  0. Exit")

        choice = input("\nChoose an option: ").strip().lower()
        if choice in ("0", "q", "quit", "exit"):
            print(f"\n{Fore.GREEN}Goodbye! 🚇")
            break

        if choice == "2":
            list_stations_menu(stations, line_groups)
            continue

        if choice == "3" and last_origin and last_destination:
            start_id = last_origin
            goal_id = last_destination
        elif choice == "1":
            print("\n" + "-" * 56)
            print(
                f"{Fore.YELLOW}Tip: Type part of the station name, I'll fuzzy match it."
            )
            start_id = get_user_selection(stations, "Origin Station:")
            if not start_id:
                continue
            goal_id = get_user_selection(stations, "Destination Station:")
            if not goal_id:
                continue
            last_origin = start_id
            last_destination = goal_id
        else:
            print(f"{Fore.RED}Invalid choice.")
            continue

        path, total_seconds = dijkstra(adj, start_id, goal_id)

        if not path:
            print(f"{Fore.RED}No route found (Graph disconnected).")
            continue

        origin_name = stations[start_id]["display_name"]
        dest_name = stations[goal_id]["display_name"]

        print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ Route Found:\n")
        dist = 0.0
        for i in range(len(path)):
            s = stations[path[i]]
            if i > 0:
                prev = stations[path[i - 1]]
                dist += haversine_km(
                    s["lat"], s["lon"], prev["lat"], prev["lon"]
                )

            meta = f"[{','.join(s['lines'])}]"
            print(f"  {i + 1:2d}. {s['display_name']} {Style.DIM}{meta}")

        num_stops = len(path) - 1
        num_interchanges = compute_interchanges(path, stations)

        now = datetime.now()
        trip_time = timedelta(seconds=total_seconds)

        print(f"\n{Fore.WHITE}{Style.BRIGHT}Summary:")
        print(f"  Current Time:        {fmt_time(now)}")
        print(f"  Origin:              {origin_name}")
        print(f"  Destination:         {dest_name}")
        print(f"  Total Stops:         {num_stops}")
        print(f"  Interchanges:        {num_interchanges}")
        print(f"  Total Distance:      {dist:.2f} km")
        print(
            f"  Est. In-train Time:  {int(total_seconds // 60)} min {int(total_seconds % 60)} sec"
        )
        print(
            f"  (Timing is an estimate based only on distance & speed)"
        )

if __name__ == "__main__":
    main()
