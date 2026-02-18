#!/usr/bin/env python3
"""
Script de prueba para validar la integración de Baseten (Kimi-K2.5) con LlamaIndex
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BASETEN_API_KEY")

print("🚀 Probando integración de LlamaIndex con Baseten (Kimi-K2.5)...")

# Verificar que podemos importar la clase BasetenLLM
print("📦 Importando BasetenLLM desde interpretador_refactored...")

try:
    from interpretador_refactored import BasetenLLM
    print("✅ Importado BasetenLLM correctamente")
except ImportError as e:
    print(f"❌ Error importando BasetenLLM: {e}")
    sys.exit(1)

model_id = "moonshotai/Kimi-K2.5"

print(f"🛠️ Intentando instanciar BasetenLLM con model='{model_id}'...")

try:
    # Probar instancia para RAG (temperatura 0)
    llm_rag = BasetenLLM(
        api_key=api_key, 
        model=model_id, 
        temperature=0.0, 
        max_tokens=4096
    )
    print("✅ Instancia RAG creada exitosamente.")
    
    # Probar instancia para Escritor (temperatura 0.7)
    llm_writer = BasetenLLM(
        api_key=api_key, 
        model=model_id, 
        temperature=0.7, 
        max_tokens=16000
    )
    print("✅ Instancia Escritor creada exitosamente.")
    
    print("\n📨 Probando método 'complete' con temperatura 0 (RAG)...")
    response_rag = llm_rag.complete("Hola, responde brevemente si estás funcionando")
    print(f"✅ Respuesta RAG recibida: {response_rag.text[:100]}...")
    
    print("\n📨 Probando método 'complete' con temperatura 0.7 (Escritor)...")
    response_writer = llm_writer.complete("Escribe una frase creativa sobre las estrellas")
    print(f"✅ Respuesta Escritor recibida: {response_writer.text[:100]}...")
    
    print("\n" + "="*60)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("="*60)
    print("\nEl modelo Kimi-K2.5 está correctamente configurado y funcionando.")
    print("Parámetros utilizados:")
    print("  • RAG: temperature=0.0, max_tokens=4096")
    print("  • Escritor: temperature=0.7, max_tokens=16000")

except Exception as e:
    print(f"❌ ERROR CRÍTICO al usar BasetenLLM: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
