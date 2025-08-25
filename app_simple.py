"""
Microservicio FastAPI para Interpretación Astrológica - Versión Simplificada
Puerto: 8002
Sin RAG - Usa interpretaciones estáticas para testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import time
import random

app = FastAPI(
    title="Astro Interpretador Simple API",
    description="Microservicio simplificado para generar interpretaciones astrológicas",
    version="1.0.0-simple"
)

# Configurar CORS para permitir requests desde Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class CartaNatalData(BaseModel):
    """Datos de carta natal recibidos del microservicio de cálculo"""
    nombre: str
    points: Dict[str, Any]
    houses: Dict[str, Any]
    aspects: List[Dict[str, Any]]

class InterpretacionRequest(BaseModel):
    """Request para generar interpretación"""
    carta_natal: CartaNatalData
    genero: str  # "masculino" o "femenino"

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

# Interpretaciones estáticas de ejemplo
INTERPRETACIONES_ESTATICAS = {
    "Sol": {
        "Aries": "Tu Sol en Aries te otorga una personalidad dinámica y emprendedora. Eres una persona que toma la iniciativa y no teme enfrentar nuevos desafíos.",
        "Tauro": "Con tu Sol en Tauro, posees una naturaleza estable y determinada. Valoras la seguridad y tienes una gran capacidad para materializar tus objetivos.",
        "Géminis": "Tu Sol en Géminis te hace una persona curiosa y comunicativa. Tienes facilidad para adaptarte a diferentes situaciones y conectar con otros.",
        "Cáncer": "Con el Sol en Cáncer, eres una persona emotiva y protectora. Tu intuición es muy desarrollada y tienes un fuerte vínculo con la familia.",
        "Leo": "Tu Sol en Leo te otorga carisma y creatividad natural. Tienes una personalidad magnética y disfrutas siendo el centro de atención.",
        "Virgo": "Con tu Sol en Virgo, eres detallista y perfeccionista. Tienes una mente analítica y gran capacidad para organizar y mejorar las cosas.",
        "Libra": "Tu Sol en Libra te hace buscar el equilibrio y la armonía. Tienes un sentido estético desarrollado y valoras las relaciones justas.",
        "Escorpio": "Con el Sol en Escorpio, posees una intensidad emocional profunda. Tienes gran capacidad de transformación y regeneración.",
        "Sagitario": "Tu Sol en Sagitario te otorga un espíritu aventurero y filosófico. Buscas constantemente expandir tus horizontes y conocimientos.",
        "Capricornio": "Con tu Sol en Capricornio, eres ambicioso y disciplinado. Tienes una gran capacidad para alcanzar metas a largo plazo.",
        "Acuario": "Tu Sol en Acuario te hace una persona innovadora y humanitaria. Valoras la libertad y tienes ideas originales.",
        "Piscis": "Con el Sol en Piscis, eres intuitivo y compasivo. Tienes una gran sensibilidad artística y espiritual."
    },
    "Luna": {
        "Aries": "Tu Luna en Aries indica emociones intensas y reacciones rápidas. Necesitas acción y movimiento para sentirte emocionalmente equilibrado.",
        "Tauro": "Con la Luna en Tauro, buscas estabilidad emocional y comodidad. Te nutres a través de los placeres sensoriales y la rutina.",
        "Géminis": "Tu Luna en Géminis te hace emocionalmente curioso y versátil. Necesitas variedad y comunicación para sentirte satisfecho.",
        "Cáncer": "Con la Luna en Cáncer, tus emociones son profundas y protectoras. El hogar y la familia son fundamentales para tu bienestar.",
        "Leo": "Tu Luna en Leo busca reconocimiento emocional y expresión creativa. Necesitas sentirte especial y apreciado.",
        "Virgo": "Con la Luna en Virgo, procesas las emociones de manera práctica y analítica. Buscas orden y utilidad en tu vida emocional.",
        "Libra": "Tu Luna en Libra necesita armonía y belleza para sentirse bien. Las relaciones equilibradas son esenciales para tu bienestar.",
        "Escorpio": "Con la Luna en Escorpio, vives las emociones con gran intensidad. Necesitas profundidad y autenticidad en tus vínculos.",
        "Sagitario": "Tu Luna en Sagitario busca aventura y significado emocional. Necesitas libertad y expansión para sentirte pleno.",
        "Capricornio": "Con la Luna en Capricornio, estructuras tus emociones de manera práctica. Buscas seguridad y logros tangibles.",
        "Acuario": "Tu Luna en Acuario te hace emocionalmente independiente y original. Valoras la libertad emocional y las causas humanitarias.",
        "Piscis": "Con la Luna en Piscis, eres extremadamente sensible e intuitivo. Necesitas conexión espiritual y compasión."
    }
}

def traducir_signo(signo_en: str) -> str:
    """Traducir signo del inglés al español"""
    traducciones = {
        "Aries": "Aries", "Taurus": "Tauro", "Gemini": "Géminis", "Cancer": "Cáncer",
        "Leo": "Leo", "Virgo": "Virgo", "Libra": "Libra", "Scorpio": "Escorpio",
        "Sagittarius": "Sagitario", "Capricorn": "Capricornio", "Aquarius": "Acuario",
        "Pisces": "Piscis"
    }
    return traducciones.get(signo_en, signo_en)

def traducir_planeta(planeta_en: str) -> str:
    """Traducir planeta del inglés al español"""
    traducciones = {
        "Sun": "Sol", "Moon": "Luna", "Mercury": "Mercurio", "Venus": "Venus", "Mars": "Marte",
        "Jupiter": "Júpiter", "Saturn": "Saturno", "Uranus": "Urano", "Neptune": "Neptuno",
        "Pluto": "Plutón"
    }
    return traducciones.get(planeta_en, planeta_en)

def generar_interpretaciones_simples(carta_natal: Dict[str, Any], genero: str) -> Dict[str, Any]:
    """Generar interpretaciones usando datos estáticos"""
    start_time = time.time()
    
    interpretaciones_individuales = []
    
    # Procesar planetas en signos
    if "points" in carta_natal:
        for planeta_en, datos in carta_natal["points"].items():
            if planeta_en in ["Sun", "Moon", "Mercury", "Venus", "Mars"] and "sign" in datos:
                planeta_es = traducir_planeta(planeta_en)
                signo_en = datos["sign"]
                signo_es = traducir_signo(signo_en)
                
                # Buscar interpretación estática
                interpretacion = "Esta es una interpretación de ejemplo para testing del sistema."
                if planeta_en in INTERPRETACIONES_ESTATICAS and signo_es in INTERPRETACIONES_ESTATICAS[planeta_en]:
                    interpretacion = INTERPRETACIONES_ESTATICAS[planeta_en][signo_es]
                
                # Formatear grados si están disponibles
                grados_str = ""
                if "degrees" in datos and datos["degrees"] is not None:
                    grados = int(datos["degrees"])
                    minutos = int((datos["degrees"] - grados) * 60)
                    grados_str = f"{grados}° {minutos:02d}'"
                
                titulo = f"Tu {planeta_es} en {signo_es}"
                if grados_str:
                    titulo = f"Tu {planeta_es} se encuentra a {grados_str} de {signo_es}"
                
                item = InterpretacionItem(
                    titulo=titulo,
                    tipo="PlanetaEnSigno",
                    interpretacion=interpretacion,
                    planeta=planeta_es,
                    signo=signo_es,
                    grados=grados_str if grados_str else None
                )
                interpretaciones_individuales.append(item)
    
    # Generar interpretación narrativa simple
    nombre = carta_natal.get("nombre", "Usuario")
    pronombre = "ella" if genero.lower() == "femenino" else "él"
    
    interpretacion_narrativa = f"""
Estimado/a {nombre},

Tu carta natal revela aspectos fascinantes de tu personalidad y potencial. A través del análisis de las posiciones planetarias en el momento de tu nacimiento, podemos comprender mejor tus características únicas.

{interpretaciones_individuales[0].interpretacion if interpretaciones_individuales else "Tu carta natal muestra una combinación única de energías planetarias."}

Esta interpretación es generada por el sistema de testing. Las interpretaciones completas con RAG estarán disponibles una vez resueltos los conflictos de dependencias.

El análisis de tu carta natal es una herramienta valiosa para el autoconocimiento y el crecimiento personal. Cada planeta y signo aporta matices únicos a tu personalidad.

Recuerda que la astrología es una guía, y tú tienes el poder de crear tu propio destino.
    """.strip()
    
    end_time = time.time()
    tiempo_generacion = end_time - start_time
    
    return {
        "interpretacion_narrativa": interpretacion_narrativa,
        "interpretaciones_individuales": interpretaciones_individuales,
        "tiempo_generacion": tiempo_generacion
    }

# Endpoints
@app.get("/health")
async def health_check():
    """Health check del microservicio"""
    return {
        "status": "healthy",
        "service": "astro-interpretador-simple",
        "version": "1.0.0-simple",
        "mode": "static_interpretations"
    }

@app.post("/interpretar", response_model=InterpretacionResponse)
async def generar_interpretacion(request: InterpretacionRequest):
    """
    Generar interpretación astrológica simplificada
    """
    try:
        print(f"🔍 Generando interpretación simple para: {request.carta_natal.nombre}")
        print(f"👤 Género: {request.genero}")
        
        # Generar interpretaciones usando datos estáticos
        resultado = generar_interpretaciones_simples(
            carta_natal_data=request.carta_natal.dict(),
            genero=request.genero
        )
        
        print(f"✅ Interpretación simple generada en {resultado['tiempo_generacion']:.2f} segundos")
        
        return InterpretacionResponse(
            interpretacion_narrativa=resultado["interpretacion_narrativa"],
            interpretaciones_individuales=resultado["interpretaciones_individuales"],
            tiempo_generacion=resultado["tiempo_generacion"]
        )
        
    except Exception as e:
        print(f"❌ Error al generar interpretación simple: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar interpretación: {str(e)}")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Astro Interpretador Simple API",
        "version": "1.0.0-simple",
        "mode": "static_interpretations",
        "note": "Versión simplificada para testing - Sin RAG",
        "endpoints": {
            "health": "/health",
            "interpretar": "/interpretar",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app_simple:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
