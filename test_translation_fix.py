import asyncio
from interpretador_refactored import InterpretadorRAG
from interpretador_astrologico import InterpretadorAstrologico

print("--- Data Payload for 26/12/1964 21:12 Buenos Aires ---")

# Mock Payload simulating the Microservice Output
payload = {
    "nombre": "Test User",
    "fecha_hora_natal": "1964-12-26T21:12:00",
    "latitud": -34.6037,
    "longitud": -58.3816,
    "tipo_carta": "draco", # IMPORTANT for triggering Draco logic
    "points": {
        "Sun": {"sign": "Libra", "deg": 10.5},
        "Moon": {"sign": "Cancer", "deg": 25.2},
        "Mercury": {"sign": "Sagittarius", "deg": 18.9},
        "Venus": {"sign": "Sagittarius", "deg": 9.6},
        "Mars": {"sign": "Virgo", "deg": 22.3},
        "Jupiter": {"sign": "Taurus", "deg": 16.4},
        "Saturn": {"sign": "Pisces", "deg": 0.8},
        "Uranus": {"sign": "Virgo", "deg": 14.8},
        "Neptune": {"sign": "Scorpio", "deg": 19.1},
        "Pluto": {"sign": "Virgo", "deg": 16.3},
        "Asc": {"sign": "Taurus", "deg": 22.4} 
    },
    "cuspides_cruzadas": [], # Auto-calculated fallback test
    "tropical_houses": {
        "1": 135.0, 
        "2": 165.0, 
        "3": 200.0, 
        "4": 235.0, 
        "5": 270.0, 
        "6": 305.0, 
        "7": 315.0, 
        "8": 345.0, 
        "9": 20.0,  
        "10": 55.0, 
        "11": 90.0, 
        "12": 125.0 
    },
    "aspectos_cruzados": [
        # User supplied list - VALID items (Conjunction/Opposition)
        {"punto_draconico": "Neptune", "punto_tropical": "Saturn", "tipo_aspecto": "Opposition"},
        {"punto_draconico": "Uranus", "punto_tropical": "Mercury", "tipo_aspecto": "Opposition"},
        {"punto_draconico": "Saturn", "punto_tropical": "Venus", "tipo_aspecto": "Conjunction"},
        {"punto_draconico": "Mars", "punto_tropical": "Sun", "tipo_aspecto": "Opposition"},
        {"punto_draconico": "Venus", "punto_tropical": "Pluto", "tipo_aspecto": "Conjunction"},
        {"punto_draconico": "Venus", "punto_tropical": "Uranus", "tipo_aspecto": "Conjunction"},
        {"punto_draconico": "Venus", "punto_tropical": "Mars", "tipo_aspecto": "Conjunction"},
        {"punto_draconico": "Mercury", "punto_tropical": "Mars", "tipo_aspecto": "Conjunction"},
        {"punto_draconico": "Sun", "punto_tropical": "Moon", "tipo_aspecto": "Conjunction"}
    ]
}

async def run_test():
    # 1. Initialize Wrapper (refactored)
    wrapper = InterpretadorRAG()
    
    # 2. Check if internal JSON engine is loaded
    if wrapper.interpretador_astrologico:
        print(f"✅ InterpretadorAstrologico integrado en InterpretadorRAG")
    else:
        print(f"❌ ERROR: InterpretadorAstrologico NO integrado")
        return

    # 3. Generate Interpretation using the Wrapper's method
    # This tests the full flow: Wrapper -> Detects Draco -> Calls JSON Engine -> Returns List
    print(f"\n--- Generating Draconic Interpretation for 26/12/1964 ---")
    print(f"DEBUG: tipo_carta will be: draco")
    result = await wrapper.generar_interpretacion_completa(payload, genero="masculino", tipo_carta="draco")
    
    interpretations = result.get("interpretaciones_individuales", [])
    narrative = result.get("interpretacion_narrativa", "")
    
    print(f"✅ Se obtuvieron {len(interpretations)} interpretaciones.")
    
    # Validation
    titles = [i['titulo'] for i in interpretations]
    print("\nGenerated Titles:")
    for t in titles:
        print(f"- {t}")

if __name__ == "__main__":
    asyncio.run(run_test())
