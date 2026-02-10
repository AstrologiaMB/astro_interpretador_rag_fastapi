import asyncio
import time
import os
import sys
from typing import Dict, Any

# Ensure we can import from local directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interpretador_refactored import InterpretadorRAG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main():
    print("🚀 Initializing InterpretadorRAG...")
    start_init = time.time()
    interpretador = InterpretadorRAG()
    end_init = time.time()
    print(f"✅ Initialization took {end_init - start_init:.2f} seconds")

    # Mock Carta Natal Data (Realistic Payload)
    carta_natal_data = {
        "nombre": "Test User",
        "fecha_hora_natal": "1990-01-01T12:00:00",
        "location": {"lat": 40.7128, "lon": -74.0060},
        "points": {
            "Sun": {"sign": "Capricorn", "longitude": 280.5, "house": 10},
            "Moon": {"sign": "Aquarius", "longitude": 315.2, "house": 11},
            "Mercury": {"sign": "Capricorn", "longitude": 285.1, "house": 10, "retrograde": True},
            "Venus": {"sign": "Aquarius", "longitude": 310.2, "house": 11},
            "Mars": {"sign": "Sagittarius", "longitude": 250.3, "house": 9},
            "Jupiter": {"sign": "Cancer", "longitude": 100.4, "house": 4},
            "Saturn": {"sign": "Capricorn", "longitude": 295.5, "house": 10},
            "Uranus": {"sign": "Capricorn", "longitude": 298.1, "house": 10},
            "Neptune": {"sign": "Capricorn", "longitude": 299.2, "house": 10},
            "Pluto": {"sign": "Scorpio", "longitude": 230.3, "house": 8},
            "Asc": {"sign": "Aries", "longitude": 15.0},
            "MC": {"sign": "Capricorn", "longitude": 285.0}
        },
        "houses": {
            "1": {"sign": "Aries", "longitude": 15.0},
            "2": {"sign": "Taurus", "longitude": 45.0},
            "3": {"sign": "Gemini", "longitude": 75.0},
            "4": {"sign": "Cancer", "longitude": 105.0},
            "5": {"sign": "Leo", "longitude": 135.0},
            "6": {"sign": "Virgo", "longitude": 165.0},
            "7": {"sign": "Libra", "longitude": 195.0},
            "8": {"sign": "Scorpio", "longitude": 225.0},
            "9": {"sign": "Sagittarius", "longitude": 255.0},
            "10": {"sign": "Capricorn", "longitude": 285.0},
            "11": {"sign": "Aquarius", "longitude": 315.0},
            "12": {"sign": "Pisces", "longitude": 345.0}
        },
        "aspects": [
            {"point1": "Sun", "point2": "Mercury", "aspect": "Conjunción", "orb": 4.6},
            {"point1": "Sun", "point2": "Jupiter", "aspect": "Oposición", "orb": 0.1},
            {"point1": "Moon", "point2": "Venus", "aspect": "Conjunción", "orb": 5.0},
            {"point1": "Mars", "point2": "Pluto", "aspect": "Sextil", "orb": 2.0},
            {"point1": "Sol", "point2": "Saturno", "aspect": "Conjunción", "orb": 3.0} # Mixed language just in case
        ]
    }

    print("\n🏁 Starting Interpretation Generation...")
    start_gen = time.time()
    
    try:
        resultado = await interpretador.generar_interpretacion_completa(
            carta_natal_data=carta_natal_data,
            genero="masculino",
            tipo_carta="tropical"
        )
        end_gen = time.time()
        print(f"\n✅ Interpretation Generation took {end_gen - start_gen:.2f} seconds")
        
        individuales = resultado.get("interpretaciones_individuales", [])
        print(f"📊 Generated {len(individuales)} individual interpretations.")
        
        narrativa = resultado.get("interpretacion_narrativa", "")
        print(f"📝 Narrative Length: {len(narrativa)} chars")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
