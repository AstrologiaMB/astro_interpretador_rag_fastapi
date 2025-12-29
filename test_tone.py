import requests
import json
import time

URL = "http://localhost:8002/interpretar-eventos"

payload = {
    "eventos": [{
        "fecha_utc": "2024-01-01",
        "hora_utc": "12:00",
        "tipo_evento": "PlanetaEnSigno",
        "descripcion": "Sol en Aries",
        "signo": "Aries", 
        "planeta": "Sol"
    }]
}

print(f"📡 Conectando a {URL}...")
print("Payload:", json.dumps(payload, indent=2))

try:
    # Retry mechanism in case services are still starting
    for i in range(5):
        try:
            response = requests.post(URL, json=payload, timeout=30)
            if response.status_code == 200:
                print("\n✅ API Respondió 200 OK")
                print("-" * 50)
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
                print("-" * 50)
                break
            else:
                print(f"⚠️ API Error: {response.status_code} - {response.text}")
                break
        except requests.exceptions.ConnectionError:
            print(f"⏳ Intento {i+1}/5: Conexión fallida (servicio iniciando?), reintentando en 3s...")
            time.sleep(3)
    else:
        print("❌ No se pudo conectar a la API después de varios intentos.")

except Exception as e:
    print(f"❌ Error inesperado: {e}")
