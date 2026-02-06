import json
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from strict_models import (
    CartaNatalData,
    InterpretacionRequest,
    InterpretacionResponse,
    InterpretacionItem,
    EventoCalendario,
    InterpretacionEventoRequest,
    InterpretacionEventosResponse,
    EventoInterpretado
)

app = FastAPI()

@app.post("/interpretar", response_model=InterpretacionResponse)
async def generar_interpretacion(request: InterpretacionRequest):
    pass

@app.post("/interpretar-eventos", response_model=InterpretacionEventosResponse)
async def interpretar_eventos_calendario(request: InterpretacionEventoRequest):
    pass

def generate_openapi_spec():
    openapi_schema = get_openapi(
        title="Astro Interpretador RAG API Strict",
        version="1.0.0",
        description="Esquema estricto para generación de clientes",
        routes=app.routes,
    )
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("OpenAPI spec generated at openapi.json")

if __name__ == "__main__":
    generate_openapi_spec()
