#!/usr/bin/env python3
"""
Script de validación para el modelo Baseten (Kimi-K2.5)
Valida que la conexión funcione correctamente.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BASETEN_API_KEY")

if not api_key:
    print("❌ Error: BASETEN_API_KEY not found.")
    exit(1)

# Modelo a validar
model_id = "moonshotai/Kimi-K2.5"

print(f"🚀 Iniciando validación del modelo Baseten...")
print(f"🔑 API Key detectada (primeros 10 chars): {api_key[:10]}...")
print(f"🤖 Modelo: {model_id}")

# Usar el endpoint compatible con OpenAI de Baseten
from openai import OpenAI

print(f"\n🛠️ Intentando conectar con Baseten...")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://inference.baseten.co/v1"
    )
    
    print("📨 Enviando mensaje de prueba...")
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "Hola, responde brevemente 'Conexión exitosa'"}],
        max_tokens=50,
        temperature=0.0
    )
    
    result = response.choices[0].message.content
    print(f"✅ ÉXITO: Conexión establecida!")
    print(f"📨 Respuesta: {result}")
    
    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)
    print(f"✅ Modelo '{model_id}' válido y funcionando")
    print(f"✅ API Key correcta")
    print(f"✅ Endpoint accesible")
    
except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
    import traceback
    traceback.print_exc()
