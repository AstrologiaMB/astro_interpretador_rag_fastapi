
import asyncio
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interpretador_refactored import InterpretadorRAG

async def reproduce_draco_error():
    print("🚀 Initializing InterpretadorRAG...")
    try:
        rag = InterpretadorRAG()
    except Exception as e:
        print(f"❌ Error initializing InterpretadorRAG: {e}")
        return

    print("✅ InterpretadorRAG initialized.")

    # Dummy Draconic Chart Data
    # Based on what I saw in code usage
    chart_data = {
        "nombre": "Test Draco",
        "points": {
            "Sun": {"sign": "Aries", "deg": 10},
            "Moon": {"sign": "Taurus", "deg": 5},
            "Asc": {"sign": "Gemini", "deg": 15}
        },
        "houses": {
            "1": {"longitude": 75},
            "2": {"longitude": 105},
        },
        "aspects": [],
        "cuspides_cruzadas": [
            {"casa_draconica": 1, "casa_tropical_ubicacion": 10},
            {"casa_draconica": 2, "casa_tropical_ubicacion": 11}
        ],
        "aspectos_cruzados": [
            {"punto_draconico": "Sun", "punto_tropical": "Moon", "tipo_aspecto": "Conjunción"}
        ]
    }

    try:
        print("🚀 Generating Draconic Interpretation...")
        result = await rag.generar_interpretacion_completa(
            carta_natal_data=chart_data,
            genero="masculino",
            tipo_carta="draco"
        )
        print("✅ Interpretation successful!")
        print(result.keys())
    except Exception as e:
        print(f"❌ Error reproducing issue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(reproduce_draco_error())
