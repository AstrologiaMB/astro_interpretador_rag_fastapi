"""
Microservicio FastAPI para Interpretación Astrológica RAG
Puerto: 8002
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import sys
from pathlib import Path

# Importar la lógica del interpretador RAG refactorizado
from interpretador_refactored import InterpretadorRAG

app = FastAPI(
    title="Astro Interpretador RAG API",
    description="Microservicio para generar interpretaciones astrológicas usando RAG",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde Next.js
# Railway-compatible: uses environment variable with localhost fallback
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del interpretador RAG
interpretador = None

@app.on_event("startup")
async def startup_event():
    """Inicializar el interpretador RAG al arrancar el servidor"""
    global interpretador
    try:
        print("🚀 Inicializando Interpretador RAG...")
        interpretador = InterpretadorRAG()
        print("✅ Interpretador RAG inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar Interpretador RAG: {e}")
        sys.exit(1)

# Modelos Pydantic
class CartaNatalData(BaseModel):
    """Datos de carta natal recibidos del microservicio de cálculo"""
    nombre: str
    points: Dict[str, Any]
    houses: Dict[str, Any]
    aspects: List[Dict[str, Any]]
    cuspides_cruzadas: Optional[List[Dict[str, Any]]] = None
    aspectos_cruzados: Optional[List[Dict[str, Any]]] = None

class InterpretacionRequest(BaseModel):
    """Request para generar interpretación"""
    carta_natal: CartaNatalData
    genero: str  # "masculino" o "femenino"
    tipo: str = "tropical"  # "tropical" o "draco" para determinar qué títulos usar

class InterpretacionItem(BaseModel):
    """Item individual de interpretación"""
    titulo: str
    tipo: str
    interpretacion: str
    planeta: Optional[str] = None
    signo: Optional[str] = None
    casa: Optional[str] = None
    aspecto: Optional[str] = None
    planeta1: Optional[str] = None
    planeta2: Optional[str] = None
    grados: Optional[str] = None

class InterpretacionResponse(BaseModel):
    """Respuesta con interpretaciones completas"""
    interpretacion_narrativa: str
    interpretaciones_individuales: List[InterpretacionItem]
    tiempo_generacion: float

# --- Modelos para Interpretación de Eventos de Calendario ---

class EventoCalendario(BaseModel):
    """
    Representa un único evento de calendario que necesita interpretación.
    Es un espejo del modelo AstroEventResponse del servicio de calendario.
    """
    fecha_utc: str
    hora_utc: str
    tipo_evento: str
    descripcion: str
    planeta1: Optional[str] = None
    planeta2: Optional[str] = None
    posicion1: Optional[str] = None
    posicion2: Optional[str] = None
    tipo_aspecto: Optional[str] = None
    orbe: Optional[str] = None
    es_aplicativo: Optional[str] = None
    harmony: Optional[str] = None
    elevacion: Optional[str] = ""
    azimut: Optional[str] = ""
    signo: Optional[str] = None
    grado: Optional[str] = None
    posicion: Optional[str] = None
    casa_natal: Optional[int] = None
    house_transits: Optional[List[Dict[str, Any]]] = None
    interpretacion: Optional[str] = None

class InterpretacionEventoRequest(BaseModel):
    """Request para interpretar una lista de eventos de calendario."""
    eventos: List[EventoCalendario]

class EventoInterpretado(BaseModel):
    """Representa un evento de calendario con su interpretación."""
    descripcion: str
    interpretacion: Optional[str] = None

class InterpretacionEventosResponse(BaseModel):
    """Respuesta con una lista de eventos y sus interpretaciones."""
    interpretaciones: List[EventoInterpretado]
    tiempo_generacion: float

# --- Endpoints ---

@app.get("/health")
async def health_check():
    """Health check del microservicio"""
    global interpretador
    if interpretador is None:
        raise HTTPException(status_code=503, detail="Interpretador RAG no inicializado")
    
    return {
        "status": "healthy",
        "service": "astro-interpretador-rag",
        "version": "1.0.0",
        "rag_initialized": interpretador is not None,
        "commit_sha": os.getenv("COMMIT_SHA")
    }

@app.post("/interpretar", response_model=InterpretacionResponse)
async def generar_interpretacion(request: InterpretacionRequest):
    """
    Generar interpretación astrológica completa
    """
    global interpretador
    if interpretador is None:
        raise HTTPException(status_code=503, detail="Interpretador RAG no inicializado")
    
    try:
        print(f"🔍 Generando interpretación para: {request.carta_natal.nombre}")
        print(f"👤 Género: {request.genero}")
        
        # TEMPORAL: Guardar JSON entrante para diagnóstico (comentado para producción)
        # import json
        # with open("last_carta_received.json", "w", encoding="utf-8") as f:
        #     json.dump(request.carta_natal.dict(), f, indent=2, ensure_ascii=False)
        # print("📝 JSON de carta natal guardado en last_carta_received.json")
        
        # Generar interpretaciones usando el RAG
        resultado = await interpretador.generar_interpretacion_completa(
            carta_natal_data=request.carta_natal.dict(),
            genero=request.genero,
            tipo_carta=request.tipo
        )
        
        print(f"✅ Interpretación generada en {resultado['tiempo_generacion']:.2f} segundos")
        
        return InterpretacionResponse(
            interpretacion_narrativa=resultado["interpretacion_narrativa"],
            interpretaciones_individuales=resultado["interpretaciones_individuales"],
            tiempo_generacion=resultado["tiempo_generacion"]
        )
        
    except Exception as e:
        print(f"❌ Error al generar interpretación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar interpretación: {str(e)}")

@app.post("/interpretar-eventos", response_model=InterpretacionEventosResponse)
async def interpretar_eventos_calendario(request: InterpretacionEventoRequest):
    """
    Interpreta una lista de eventos de calendario.
    """
    import time
    start_time = time.time()
    
    global interpretador
    if interpretador is None:
        raise HTTPException(status_code=503, detail="Interpretador RAG no inicializado")

    try:
        # Tarea 1.3: Guardar JSON de eventos para diagnóstico
        import json
        # Usamos model_dump() para convertir los objetos Pydantic a diccionarios
        eventos_completos = [evento.model_dump() for evento in request.eventos]
        with open("last_events_received.json", "w", encoding="utf-8") as f:
            json.dump(eventos_completos, f, indent=2, ensure_ascii=False)
        print("📝 JSON con eventos completos guardado en last_events_received.json")

        # Lógica de interpretación (a implementar en Fase 2)
        eventos_interpretados = []
        for evento in request.eventos:
            # Llamar a la nueva función de búsqueda en el interpretador
            interpretacion = interpretador.buscar_interpretacion_evento(evento.model_dump())
            eventos_interpretados.append(EventoInterpretado(
                descripcion=evento.descripcion,
                interpretacion=interpretacion
            ))

        tiempo_generacion = time.time() - start_time
        print(f"✅ {len(eventos_interpretados)} eventos procesados en {tiempo_generacion:.2f} segundos")

        return InterpretacionEventosResponse(
            interpretaciones=eventos_interpretados,
            tiempo_generacion=tiempo_generacion
        )

    except Exception as e:
        print(f"❌ Error al interpretar eventos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al interpretar eventos: {str(e)}")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Astro Interpretador RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "interpretar": "/interpretar",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    # Railway-compatible: uses environment variable with local fallback
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
