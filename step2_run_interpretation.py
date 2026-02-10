import asyncio
import os
import sys
import json
import time

# Añadir directorio actual al path
sys.path.append(os.getcwd())

from interpretador_refactored import InterpretadorRAG

async def run_interpretation():
    print("🚀 INICIANDO INTERPRETACIÓN DE CASO REAL (BUENOS AIRES 1964)")
    
    # 1. Cargar Payload
    payload_path = "real_case_payload.json"
    if not os.path.exists(payload_path):
        print(f"❌ Error: No existe {payload_path}")
        return
        
    with open(payload_path, 'r') as f:
        payload = json.load(f)
        
    print(f"✅ Payload cargado: {payload.get('nombre')}")
    
    # 2. Inicializar Interpretador
    print("Initializing InterpretadorRAG...")
    start_init = time.time()
    rag = InterpretadorRAG()
    print(f"✅ InterpretadorRAG inicializado en {time.time() - start_init:.2f}s")
    
    # 3. Ejecutar Interpretación
    print("\n🚀 Ejecutando generar_interpretacion_completa...")
    start_gen = time.time()
    resultado = await rag.generar_interpretacion_completa(payload, genero="masculino", tipo_carta="tropical")
    total_time = time.time() - start_gen
    
    print(f"\n⏱️ Tiempo Total de Generación: {total_time:.4f}s")
    
    # 4. Mostrar Resultados Resumidos
    interpretaciones = resultado.get("interpretaciones_individuales", [])
    narrativa = resultado.get("interpretacion_narrativa", "")
    
    print(f"\n📊 Se generaron {len(interpretaciones)} interpretaciones individuales.")
    
    print("\n=== TÍTULOS GENERADOS ===")
    for i, item in enumerate(interpretaciones):
        print(f"{i+1}. [{item.get('tipo')}] {item.get('titulo')}")
        
    # 5. Guardar Resultado Completo
    output_path = "real_case_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Resultado guardado en {output_path}")

if __name__ == "__main__":
    asyncio.run(run_interpretation())
