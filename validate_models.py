import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ Error: ANTHROPIC_API_KEY not found.")
    exit(1)

# Lista larga de candidatos potenciales para 2026
candidates = [
    # --- Validated working (Control) ---
    "claude-3-5-haiku-latest",
    
    # --- User Provided Specific IDs (Testing these!) ---
    "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5-20251001",
    
    # --- Variations just in case (Standard Anthropic format vs User format) ---
    "claude-4-5-sonnet-20250929", 
    "claude-4-5-haiku-20251001",
]

print(f"🚀 Iniciando validación fehaciente de modelos Anthropic...")
print(f"🔑 API Key detectada (primeros 10 chars): {api_key[:10]}...")

headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

valid_models = []

for model in candidates:
    print(f"\nProbrando ID: '{model}' ...")
    
    # Payload mínimo
    data = {
        "model": model,
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "Hi"}]
    }
    
    try:
        response = requests.post("https://api.anthropic.com/v1/messages", json=data, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ ÉXITO: El modelo '{model}' ES VÁLIDO.")
            valid_models.append(model)
        else:
            err_msg = response.json().get('error', {}).get('message', 'Unknown error')
            if "not found" in err_msg or "multimodal" in err_msg: 
               print(f"❌ FALLÓ: {err_msg}")
            else:
               print(f"⚠️ ERROR DISTINTO: {response.status_code} - {err_msg}")
               
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

print("\n" + "="*50)
print("📊 RESUMEN FINAL DE MODELOS VÁLIDOS")
print("="*50)
for m in valid_models:
    print(f"✅ {m}")
