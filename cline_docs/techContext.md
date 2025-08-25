# Tech Context

## Technologies Used

### Core Framework
- **FastAPI**: Microservicio web framework para Python con documentación automática
- **Python 3.8+**: Lenguaje principal con compatibilidad confirmada
- **Uvicorn**: Servidor ASGI para FastAPI en puerto 8002

### RAG System
- **LlamaIndex**: Core framework for RAG implementation.
- **OpenAI Embeddings**: `text-embedding-ada-002` for semantic search.
- **OpenAI API**: `gpt-3.5-turbo` and `gpt-4-turbo-preview` for text generation.
- **re (regex)**: Critical for the flexible title matching system.

### Data Processing
- **json**: Procesamiento nativo de cartas natales y eventos del calendario.
- **pathlib**: Manejo moderno de rutas multiplataforma.
- **python-dotenv**: Gestión de variables de entorno.

### Web Framework
- **FastAPI**: Framework principal con endpoints `/interpretar` y `/interpretar-eventos`.
- **CORS**: Configurado para recibir requests desde Next.js (puerto 3000).
- **Pydantic**: Validación de datos y modelos de request/response.

## Development Setup

### Environment Configuration
```bash
# .env file required
OPENAI_API_KEY=sk-...
```

### Project Structure
```
/astro_interpretador_rag_fastapi/
├── app.py                      # 🎯 FastAPI microservice principal
├── interpretador_refactored.py # 🧠 Lógica RAG optimizada
├── requirements.txt            # 📦 Dependencias principales
├── /data/                      # 📚 Base de conocimiento
│   ├── *.md                     # Archivos de interpretación
│   └── Títulos normalizados minusculas.txt # Master list of valid titles
└── /cline_docs/               # 📝 Documentación actualizada
```

## Technical Constraints

### API Dependencies
- **Internet Required**: Conectividad para API de OpenAI.
- **Rate Limits**: Sujeto a las limitaciones de la API de OpenAI.

### Data Requirements
- **Title Matching**: The success of the calendar interpretation feature is critically dependent on the regex in `_flexible_title_match` being able to handle variations in event descriptions and match them to the master title list.

## Key Technical Decisions

### RAG Architecture
- **Semantic Search**: Utilizes LlamaIndex with OpenAI embeddings for contextual relevance.
- **Modular Knowledge**: Astrological knowledge is stored in markdown files, decoupled from the application logic.
- **Title-Based Filtering**: The system only processes events for which a valid title exists in `Títulos normalizados minusculas.txt`, ensuring quality and relevance.

### Calendar Integration Architecture
- **On-Demand Fetching**: The frontend requests interpretations for calendar events one by one upon user interaction. This is a highly performant approach that avoids overwhelming the backend.
- **Flexible Title Matching**: A sophisticated regex-based system was developed to bridge the gap between programmatically generated event titles and the human-written titles in the knowledge base. This was a critical factor for the success of the feature.

## Recent Technical Improvements

### Calendar Integration (July 2025)
- **Advanced Regex Implementation**: Developed and iteratively refined a complex regular expression in the `_flexible_title_match` function. This was the core of the debugging effort and now successfully handles various Spanish grammatical constructs (e.g., "a", "al", "a la") and compound aspects (e.g., "conjunción o cuadratura").
- **Systematic Debugging**: Employed a systematic debugging process by returning the generated title candidates to the UI. This allowed for precise identification of mismatches and guided the refinement of the regex.
- **Architectural Decision**: Solidified the "On-Demand" data fetching model (Opción A) over a less performant "Backend Enrichment" model (Opción B).

## Development Environment

### IDE/Tools
- **VSCode**: Editor principal con extensiones Python.
- **Git**: Control de versiones con commits atómicos y descriptivos.
- **Branching**: All recent development was done on the `feature/calendar-interpretation-v2` branch.

### Testing Strategy
- **Manual Iterative Testing**: The recent calendar feature was tested iteratively by feeding specific failing event titles and refining the matching logic until all known cases were handled correctly.
- **Log-Based Debugging**: The `[SIN COINCIDENCIA]` error message was a key tool for identifying failed matches during the development process.
