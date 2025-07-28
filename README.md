# Astro Interpretador RAG FastAPI

Microservicio FastAPI para interpretaciones astrológicas usando RAG (Retrieval-Augmented Generation). Este servicio interactúa con [homepageastrowellness](https://github.com/AstrologiaMB/homepageastrowellness) para proporcionar interpretaciones inteligentes de cartas natales, tránsitos y eventos astrológicos.

## 🌟 Características

- **API RESTful** con FastAPI para interpretaciones astrológicas
- **Sistema RAG** (Retrieval-Augmented Generation) para respuestas contextuales
- **Base de conocimiento modular** con 22+ archivos de interpretaciones especializadas
- **Normalización inteligente** de títulos astrológicos
- **Soporte completo** para planetas, aspectos, casas y tránsitos
- **Integración perfecta** con el frontend Next.js

## 🏗️ Arquitectura

Este microservicio forma parte del ecosistema Astrowellness:

```
┌─────────────────────────────────────┐
│     homepageastrowellness           │
│     (Frontend Next.js)              │
└─────────────┬───────────────────────┘
              │ HTTP Requests
              ▼
┌─────────────────────────────────────┐
│  astro_interpretador_rag_fastapi    │
│  (Este Microservicio)               │
│                                     │
│  ┌─────────────────────────────┐    │
│  │     InterpretadorRAG        │    │
│  │   - Búsqueda semántica      │    │
│  │   - Normalización títulos   │    │
│  │   - Matching inteligente    │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │   Base de Conocimiento      │    │
│  │   - 22 archivos modulares   │    │
│  │   - 711+ títulos únicos     │    │
│  │   - Interpretaciones ricas  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip o conda

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/AstrologiaMB/astro_interpretador_rag_fastapi.git
   cd astro_interpretador_rag_fastapi
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8002 --reload
   ```

El servicio estará disponible en `http://localhost:8002`

## 📚 API Endpoints

### Health Check
```http
GET /health
```

### Interpretación de Eventos
```http
POST /interpretar-eventos
Content-Type: application/json

{
  "eventos": [
    {
      "titulo": "sol en tránsito conjunción a venus natal",
      "fecha": "2025-01-15",
      "tipo": "transito"
    }
  ]
}
```

### Documentación Interactiva

- **Swagger UI**: `http://localhost:8002/docs`
- **ReDoc**: `http://localhost:8002/redoc`

## 🧠 Sistema RAG

### Base de Conocimiento

El sistema utiliza una base de conocimiento modular organizada en archivos especializados:

- **Planetas**: Sol, Luna, Mercurio, Venus, Marte, Júpiter, Saturno, Urano, Neptuno, Plutón
- **Puntos especiales**: Nodos lunares, Lilith, Almuten Figuris
- **Casas astrológicas**: 12 casas con interpretaciones detalladas
- **Aspectos**: Conjunción, oposición, cuadratura, trígono, sextil
- **Tránsitos**: Interpretaciones dinámicas de movimientos planetarios
- **Configuraciones**: Patrones astrológicos complejos

### Normalización Inteligente

El sistema incluye un normalizador avanzado que:

- Convierte títulos a formato estándar
- Maneja sinónimos y variaciones
- Procesa aspectos y planetas retrógrados
- Optimiza la búsqueda semántica

### Algoritmo de Matching

1. **Normalización** del título de entrada
2. **Búsqueda exacta** en la base de títulos
3. **Búsqueda semántica** con similitud de texto
4. **Fallback inteligente** para casos no encontrados
5. **Respuesta contextual** basada en el mejor match

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` (opcional):

```env
# Puerto del servidor
PORT=8002

# Nivel de logging
LOG_LEVEL=INFO

# Configuración de CORS
CORS_ORIGINS=["http://localhost:3000"]
```

### Archivos de Configuración

- `requirements.txt`: Dependencias Python
- `.gitignore`: Archivos excluidos del control de versiones
- `cline_docs/`: Documentación del proyecto y contexto

## 📁 Estructura del Proyecto

```
astro_interpretador_rag_fastapi/
├── app.py                          # Aplicación FastAPI principal
├── interpretador_refactored.py     # Motor RAG refactorizado
├── normalize_astro_titles.py       # Normalizador de títulos
├── mostrar_archivos_cargados.py    # Utilidad de diagnóstico
├── requirements.txt                # Dependencias Python
├── .gitignore                     # Exclusiones Git
├── README.md                      # Este archivo
├── data/                          # Base de conocimiento
│   ├── 1 - introducción carta natal.md
│   ├── 2 - el sol_ la identidad.md
│   ├── 3 - la luna_ las emociones.md
│   ├── ...                        # 22+ archivos modulares
│   └── Títulos normalizados minusculas.txt
└── cline_docs/                    # Documentación del proyecto
    ├── productContext.md
    ├── activeContext.md
    ├── systemPatterns.md
    ├── techContext.md
    └── progress.md
```

## 🔗 Integración con homepageastrowellness

Este microservicio está diseñado para integrarse perfectamente con el frontend Next.js:

### Endpoints Consumidos por el Frontend

1. **Interpretación de Eventos del Calendario**
   - Recibe eventos astrológicos calculados
   - Devuelve interpretaciones enriquecidas
   - Utilizado en `/calendario/personal`

2. **Interpretación de Cartas Natales**
   - Procesa elementos de cartas natales
   - Proporciona análisis detallados
   - Utilizado en `/cartas/tropica`

### Flujo de Datos

```
Frontend (Next.js) → API Request → FastAPI → RAG Engine → Knowledge Base → Response → Frontend
```

## 🧪 Testing

### Ejecutar Tests
```bash
pytest
```

### Test de Health Check
```bash
curl http://localhost:8002/health
```

### Test de Interpretación
```bash
curl -X POST http://localhost:8002/interpretar-eventos \
  -H "Content-Type: application/json" \
  -d '{"eventos": [{"titulo": "sol en casa 1", "fecha": "2025-01-01", "tipo": "natal"}]}'
```

## 📊 Monitoreo y Logs

El servicio incluye logging detallado para:

- Inicialización del sistema RAG
- Carga de la base de conocimiento
- Procesamiento de requests
- Errores y excepciones
- Métricas de performance

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte del ecosistema Astrowellness desarrollado por AstrologiaMB.

## 🔮 Roadmap

- [ ] Soporte para más idiomas
- [ ] Cache inteligente de interpretaciones
- [ ] Métricas avanzadas de uso
- [ ] Integración con más fuentes astrológicas
- [ ] API versioning
- [ ] Documentación OpenAPI extendida

## 📞 Soporte

Para soporte técnico o preguntas sobre integración, contacta al equipo de desarrollo de Astrowellness.

---

**Desarrollado con ❤️ por el equipo de AstrologiaMB**
