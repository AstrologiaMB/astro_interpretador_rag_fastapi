#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de Baseten.
Ejecutar antes de iniciar el servidor para validar las credenciales.
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_baseten_connection():
    """Probar conexión a Baseten con el modelo Kimi-K2.5"""
    
    print("🧪 Probando configuración de Baseten...")
    print()
    
    # Verificar variables de entorno
    baseten_key = os.getenv("BASETEN_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print("1️⃣ Verificando variables de entorno:")
    print(f"   BASETEN_API_KEY: {'✅ Configurada' if baseten_key else '❌ No encontrada'}")
    print(f"   OPENAI_API_KEY: {'✅ Configurada' if openai_key else '❌ No encontrada'}")
    print()
    
    if not baseten_key:
        print("❌ ERROR: BASETEN_API_KEY no está configurada.")
        print("   Crea un archivo .env con: BASETEN_API_KEY=tu-api-key")
        return False
    
    if not openai_key:
        print("❌ ERROR: OPENAI_API_KEY no está configurada.")
        print("   Crea un archivo .env con: OPENAI_API_KEY=sk-tu-api-key")
        return False
    
    # Probar conexión a Baseten
    print("2️⃣ Probando conexión a Baseten...")
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=baseten_key,
            base_url="https://inference.baseten.co/v1"
        )
        
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2.5",
            messages=[{"role": "user", "content": "Hola, responde con 'Conexión exitosa'"}],
            temperature=0.0,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"   ✅ Conexión exitosa!")
        print(f"   📨 Respuesta: {result}")
        print()
        
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print()
        return False
    
    # Probar importación de llama-index
    print("3️⃣ Verificando dependencias de llama-index...")
    try:
        from llama_index.core import Settings
        from llama_index.embeddings.openai import OpenAIEmbedding
        print("   ✅ llama-index importado correctamente")
        print()
    except ImportError as e:
        print(f"   ❌ Error importando llama-index: {e}")
        print("   Ejecuta: pip install llama-index>=0.10.0")
        return False
    
    # Probar importación de BasetenLLM
    print("4️⃣ Verificando clase BasetenLLM...")
    try:
        from interpretador_refactored import BasetenLLM
        print("   ✅ BasetenLLM importado correctamente")
        print()
    except ImportError as e:
        print(f"   ❌ Error importando BasetenLLM: {e}")
        return False
    
    print("=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("=" * 60)
    print()
    print("El sistema está listo para usar Baseten con Kimi-K2.5!")
    print("Inicia el servidor con: python app.py")
    
    return True


if __name__ == "__main__":
    success = test_baseten_connection()
    sys.exit(0 if success else 1)
