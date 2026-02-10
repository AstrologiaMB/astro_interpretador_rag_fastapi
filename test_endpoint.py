import requests
import json

payload = {
    "carta_natal": {
        "nombre": "Test User",
        "fecha_hora_natal": "1990-01-01T12:00:00",
        "location": {"lat": 0, "lon": 0},
        "tipo": "Tropical",
        "points": {
            "Sun": {"sign_name": "Aries", "longitude": 0, "house": 1},
            "Moon": {"sign_name": "Taurus", "longitude": 30, "house": 2},
             "Asc": {"sign_name": "Pisces", "longitude": 330},
             "North Node": {"sign_name": "Gemini", "longitude": 60, "house": 11}
        },
        "houses": {
            "1": {"longitude": 0}, "2": {"longitude": 30}, "3": {"longitude": 60},
            "4": {"longitude": 90}, "5": {"longitude": 120}, "6": {"longitude": 150},
            "7": {"longitude": 180}, "8": {"longitude": 210}, "9": {"longitude": 240},
            "10": {"longitude": 270}, "11": {"longitude": 300}, "12": {"longitude": 330}
        },
        "aspects": []
    },
    "genero": "femenino",
    "tipo": "tropical"
}

print("🚀 Enviando request a /interpretar...")
try:
    response = requests.post("http://localhost:8006/interpretar", json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"❌ Error conectando: {e}")
