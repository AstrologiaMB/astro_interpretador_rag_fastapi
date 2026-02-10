from interpretador_astrologico import InterpretadorAstrologico

print("--- Direct Call to get_draconic_interpretations ---")

interp = InterpretadorAstrologico()
print(f"✅ Loaded {len(interp.draco_map)} draco keys")

# Mock payload matching expected format
chart_data = {
    "points": {
        "Sun": {"sign": "Libra"},
        "Moon": {"sign": "Cancer"},
        "Asc": {"sign": "Taurus"}
    },
    "houses": {},
    "tropical_houses": {
        "1": 135.0, "2": 165.0, "3": 200.0, "4": 235.0, "5": 270.0, "6": 305.0,
        "7": 315.0, "8": 345.0, "9": 20.0, "10": 55.0, "11": 90.0, "12": 125.0 
    },
    "contacts": [
        {"p1": "Neptune", "p2": "Saturn", "aspect": "Opposition"},
        {"p1": "Uranus", "p2": "Mercury", "aspect": "Opposition"},
        {"p1": "Saturn", "p2": "Venus", "aspect": "Conjunction"},
        {"p1": "Venus", "p2": "Pluto", "aspect": "Conjunction"},
        {"p1": "Venus", "p2": "Mars", "aspect": "Conjunction"},
        {"p1": "Mercury", "p2": "Mars", "aspect": "Conjunction"},
        {"p1": "Sun", "p2": "Moon", "aspect": "Conjunction"}
    ]
}

results = interp.get_draconic_interpretations(chart_data)

print(f"\n✅ Got {len(results)} interpretations")
print("\n--- TITLES ---")
for r in results:
    print(f"  - {r['titulo']}")
