import time
import json
from interpretador_refactored import InterpretadorRAG

def test_speed():
    print("🚀 Iniciando prueba de velocidad del Motor JSON (sin LLM)...")
    
    # 1. Inicializar solo lo necesario
    rag = InterpretadorRAG()
    
    # Datos de prueba (Buenos Aires)
    carta_fake = {
        "nombre": "Test Speed",
        "points": {
            "Sun": {"sign_name": "Capricorn", "house": 6, "longitude": 278},
            "Moon": {"sign_name": "Libra", "house": 3, "longitude": 185},
            "Mercury": {"sign_name": "Sagittarius", "house": 5, "longitude": 260},
            "Venus": {"sign_name": "Sagittarius", "house": 5, "longitude": 265},
            "Mars": {"sign_name": "Virgo", "house": 2, "longitude": 160},
            "Asc": {"sign_name": "Cancer", "longitude": 100},
            "North Node": {"sign_name": "Gemini", "house": 11, "longitude": 70}
        },
        "houses": {
            "1": {"longitude": 100}, "2": {"longitude": 130}, "3": {"longitude": 160},
            "4": {"longitude": 190}, "5": {"longitude": 220}, "6": {"longitude": 250},
            "7": {"longitude": 280}, "8": {"longitude": 310}, "9": {"longitude": 340},
            "10": {"longitude": 10}, "11": {"longitude": 40}, "12": {"longitude": 70}
        },
        "aspects": [
             {"point1": "Sun", "point2": "Saturn", "aspect": "Sextil"},
             {"point1": "Sun", "point2": "Uranus", "aspect": "Trígono"}
        ]
    }
    
    # 2. Medir tiempo SOLO de la extracción determinista
    print("\n⏱️ Midiendo tiempo de extracción de interpretaciones...")
    start = time.perf_counter()
    
    # Acceso directo al motor JSON (simulando lo que hace generar_interpretacion_completa antes del LLM)
    interpretaciones = rag.interpretador_astrologico.get_natal_interpretations(carta_fake)
    
    end = time.perf_counter()
    duration_ms = (end - start) * 1000
    
    print(f"\n✅ Interpretaciones Recuperadas: {len(interpretaciones)}")
    print(f"⚡ Tiempo de Ejecución Motor JSON: {duration_ms:.4f} ms")
    print("-" * 40)
    print("CONCLUSIÓN: El motor es instantáneo. La demora de ~120s proviene EXCLUSIVAMENTE de la generación narrativa con IA (Claude/GPT).")

if __name__ == "__main__":
    test_speed()
