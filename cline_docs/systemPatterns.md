# System Patterns

## Architecture Overview

### Microservice Pattern
```
Astrowellness Ecosystem (5 Microservices)
├── Next.js Frontend (Port 3000)        # 🌐 UI/UX Layer
├── Calculo Carta Natal (Port 8001)     # 🧮 Chart Calculations
├── Interpretador RAG (Port 8002)       # 🧠 THIS SERVICE
├── Astrogematria (Port 8003)           # 🔢 Numerology
└── Eventos Personales (Port 8004)      # 📅 Personal Events
```

### RAG (Retrieval-Augmented Generation) Pattern
```
Input (JSON Chart/Event) → Knowledge Retrieval → Context Augmentation → LLM Generation → Output (JSON)
```

## Core Design Patterns

### 1. FastAPI Microservice Pattern
```python
# app.py - Main FastAPI application
@app.post("/interpretar-eventos")
async def interpretar_eventos(eventos: List[dict]):
    # 1. Validate input
    # 2. Initialize RAG interpreter
    # 3. Process each event
    # 4. Return structured response
```

**Benefits:**
- **Separation of Concerns**: Cada microservicio tiene responsabilidad específica
- **Scalability**: Puede escalar independientemente
- **Technology Flexibility**: Diferentes tecnologías por servicio
- **Fault Isolation**: Fallos no afectan otros servicios

### 2. On-Demand Interpretation Pattern (for Calendar)
The system uses an "On-Demand" approach for calendar events. The frontend (`EventoConInterpretacion.tsx`) calls the `/interpretar-eventos` endpoint only when a user clicks to see an interpretation for a specific event. This is highly efficient as it avoids processing all events at once.

### 3. RAG Implementation Pattern
```python
class InterpretadorRAG:
    def __init__(self):
        self.load_knowledge_base()    # Load astrological sections
        self.setup_embeddings()       # OpenAI embeddings
        
    def buscar_interpretacion_evento(self, evento):
        titulo_candidato = self.generar_titulo_candidato(evento)
        if self._flexible_title_match(titulo_candidato):
             context = self.retrieve_context(titulo_candidato)
             interpretation = self.generate(context)
             return interpretation
        else:
             return "No match found"
```

**Benefits:**
- **Knowledge Grounding**: Interpretaciones basadas en contenido astrológico real
- **Semantic Relevance**: Búsqueda por similitud semántica, no keywords
- **Consistency**: Mismo conocimiento base para todas las interpretaciones
- **Maintainability**: Conocimiento separado del código

### 4. Modular Knowledge Base Pattern
```
/data/
├── *.md                       # Astrological interpretation files
└── Títulos normalizados minusculas.txt # Master list of all valid titles
```

**Benefits:**
- **Modularity**: Cada archivo cubre tema específico
- **Maintainability**: Fácil editar contenido sin afectar código
- **Scalability**: Agregar nuevos temas sin reestructurar
- **Version Control**: Cambios granulares en contenido

### 5. Flexible Title Matching Pattern
```python
# interpretador_refactored.py
def _flexible_title_match(self, consulta: str) -> bool:
    # 1. Try exact match first
    if consulta in self.target_titles_set:
        return True
    
    # 2. Advanced regex for transit aspects
    # Handles "a", "al", "a la" and compound aspects
    match_consulta = re.search(r'(\w+)\s+en tránsito\s+(.*?)\s+a\s+(\w+)\s+natal', consulta)
    if match_consulta:
        # ... complex regex logic to find match in titles ...
        # like "venus en tránsito cuadratura a la luna natal"
        return True

    # 3. Fallback for general aspects
    # ...
    
    return False
```

**Benefits:**
- **Robustness**: Handles grammatical variations in Spanish ("a", "al", "a la").
- **Flexibility**: Matches specific queries (e.g., "cuadratura") against compound titles (e.g., "conjunción o cuadratura u oposición").
- **Precision**: Reduces false negatives where a valid interpretation exists but the title format differs slightly.

## Data Flow Patterns

### 1. Calendar Event Interpretation Flow
```
Frontend (User Click) → POST /interpretar-eventos → FastAPI → buscar_interpretacion_evento → Flexible Title Match → RAG Query → Response JSON
```

### 2. Knowledge Retrieval Flow
```
Event Title → Normalization → Flexible Title Match → Semantic Search → Relevant Context → LLM Prompt → Interpretation
```

## Error Handling Patterns

### 1. No Match Found
If `_flexible_title_match` returns `False`, the system returns a `[SIN COINCIDENCIA]: {consulta_normalizada}` message. This is critical for debugging as it immediately shows the exact title string that failed to find a match in `Títulos normalizados minusculas.txt`.

### 2. Input Validation
Pydantic models in `app.py` ensure that incoming event data has the required structure.

## Performance Patterns

### 1. On-Demand Processing
For calendar events, interpretations are only fetched when requested by the user, which is highly performant and avoids unnecessary processing.

### 2. Lazy Loading
The `InterpretadorRAG` class loads and indexes the knowledge base only once upon initialization, making subsequent requests fast.

### 3. Optimized Matching
The `_flexible_title_match` function prioritizes an exact match check before attempting more computationally expensive regex operations.
