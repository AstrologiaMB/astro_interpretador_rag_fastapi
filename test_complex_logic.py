import asyncio
import os
import sys
from pprint import pprint

# Añadir directorio actual al path
sys.path.append(os.getcwd())

from interpretador_refactored import InterpretadorRAG
from interpretador_astrologico import InterpretadorAstrologico

async def test_complex_logic():
    print("🧪 INICIANDO TEST DE LÓGICA COMPLEJA TROPICAL")
    
    # 1. Inicializar Interpretador
    rag = InterpretadorRAG()
    
    # Verificar que se cargó el motor JSON
    if not rag.interpretador_astrologico:
        print("❌ Error: InterpretadorAstrologico no se inicializó en InterpretadorRAG.")
        return

    print("✅ InterpretadorRAG inicializado con motor JSON.")
    
    # 2. Crear Payload de Prueba (Mock)
    # Condición a probar: 
    # "sol en conjunción o cuadratura u oposición a júpiter y saturno o plutón están en casa 1 o 4 o 7 o 10"
    
    payload = {
        "nombre": "Test User",
        "fecha": "1990-01-01",
        "hora": "12:00",
        "lat": 0,
        "lon": 0,
        "points": {
            "Sun": {"sign_name": "Aries", "degrees": 15.0, "house": 1},
            "Jupiter": {"sign_name": "Cancer", "degrees": 15.0, "house": 4}, # Cuadratura al Sol
            "Saturn": {"sign_name": "Libra", "degrees": 10.0, "house": 7},   # Saturno en Casa 7 (Angular)
            "Mars": {"sign_name": "Taurus", "house": 2},
            "Venus": {"sign_name": "Pisces", "house": 12}, 
            "Moon": {"sign_name": "Leo", "house": 5},
            "Asc": {"sign_name": "Aries", "degrees": 0.0}
        },
        "houses": {
            "1": {"sign": "Aries"},
            "4": {"sign": "Cancer"},
            "7": {"sign": "Libra"},
            "10": {"sign": "Capricorn"}
        },
        "aspects": [
            {
                "p1_name": "Sun",
                "p2_name": "Jupiter",
                "type": "square",
                "orb": 0.0
            }
        ]
    }
    
    print("\n📊 Payload de prueba creado:")
    print("- Sol en Aries (Casa 1)")
    print("- Júpiter en Cáncer (Casa 4)")
    print("- Aspecto: Sol Cuadratura Júpiter")
    print("- Saturno en Casa 7 (Angular) -> DEBE ACTIVAR CLAVE COMPLEJA")
    
    # 3. Ejecutar Interpretación
    print("\n🚀 Ejecutando generar_interpretacion_completa...")
    resultado = await rag.generar_interpretacion_completa(payload, genero="masculino", tipo_carta="tropical")
    
    # 4. Verificar Resultados
    interpretaciones = resultado.get("interpretaciones_individuales", [])
    
    found_complex = False
    complex_title = "sol en conjunción o cuadratura u oposición a júpiter y saturno o plutón están en casa 1 o 4 o 7 o 10"
    
    print(f"\n🔍 Buscando clave compleja: '{complex_title}'")
    
    for item in interpretaciones:
        if item.get("titulo", "").lower() == complex_title.lower():
            found_complex = True
            print("\n✅ ¡ÉXITO! Se encontró la interpretación compleja:")
            print(f"   Título: {item['titulo']}")
            print(f"   Inicio Texto: {item['interpretacion'][:100]}...")
            break
            
    if not found_complex:
        print("\n❌ FALLO: No se encontró la clave compleja.")
        print("Interpretaciones encontradas:")
        for item in interpretaciones:
            print(f"- {item.get('titulo')}")

if __name__ == "__main__":
    asyncio.run(test_complex_logic())
