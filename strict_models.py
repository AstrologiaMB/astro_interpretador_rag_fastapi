from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

# --- Modelos para Interpretación de Carta Natal ---

class CartaNatalData(BaseModel):
    """Datos de carta natal recibidos del microservicio de cálculo"""
    nombre: str = Field(..., description="Nombre del consultante")
    points: Dict[str, Any] = Field(..., description="Datos de planetas y puntos")
    houses: Dict[str, Any] = Field(..., description="Datos de casas")
    aspects: List[Dict[str, Any]] = Field(..., description="Lista de aspectos")
    cuspides_cruzadas: Optional[List[Dict[str, Any]]] = None
    aspectos_cruzados: Optional[List[Dict[str, Any]]] = None

class InterpretacionRequest(BaseModel):
    """Request para generar interpretación"""
    carta_natal: CartaNatalData
    genero: str = Field(..., description="Género: masculino o femenino")
    tipo: str = Field("tropical", description="Tipo de carta: tropical o draco")

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
