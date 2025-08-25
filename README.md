# 🌟 Calendario Astrológico Personal - Microservicio FastAPI

Microservicio FastAPI completo para cálculos de calendario astrológico personal con tránsitos astronómicos, fases lunares, eclipses y profecciones anuales. Forma parte del ecosistema [Astrowellness](https://github.com/AstrologiaMB/homepageastrowellness) proporcionando cálculos astrológicos de alta precisión.

## 🎯 Características Principales

### ✨ **Cálculos Astrológicos Avanzados**
- **Tránsitos Astronómicos V4**: Cálculos de precisión con Swiss Ephemeris
- **Tránsitos por Casas en Tiempo Real**: Estado actual de planetas lentos
- **Luna Progresada**: Conjunciones con planetas natales
- **Profecciones Anuales**: Sistema tradicional de casas por edad
- **Fases Lunares**: Lunas nuevas y llenas con aspectos natales
- **Eclipses**: Solares y lunares con análisis de casas
- **Aspectos Dinámicos**: Conjunciones, oposiciones, cuadraturas exactas

### 🚀 **Tecnología de Vanguardia**
- **FastAPI**: API REST moderna con documentación automática
- **Swiss Ephemeris**: Máxima precisión astronómica
- **Immanuel**: Biblioteca astrológica avanzada
- **Cálculos Paralelos**: Optimización de rendimiento
- **Integración Seamless**: Con frontend React/TypeScript

### 🔮 **Características Únicas**
- **Cálculo Dinámico**: Genera carta natal automáticamente desde datos básicos
- **Tránsitos de Largo Plazo**: Júpiter, Saturno, Urano, Neptuno, Plutón por casas
- **Interpretaciones Enriquecidas**: Integración con servicio RAG de interpretaciones
- **Múltiples Calculadores**: V4 astronómico, progresado, profecciones

## 🏗️ Arquitectura del Sistema

```
astro-calendar-personal-fastapi/
├── app.py                          # FastAPI application principal
├── src/                           # Código fuente modular
│   ├── calculators/               # Motores de cálculo especializados
│   │   ├── astronomical_transits_calculator_v4.py  # ⭐ Calculador principal
│   │   ├── natal_chart.py         # Generación de cartas natales
│   │   ├── profections_calculator.py  # Profecciones anuales
│   │   ├── lunar_phases.py        # Fases lunares
│   │   ├── eclipses.py           # Eclipses solares y lunares
│   │   └── progressed_moon_transits.py  # Luna progresada
│   ├── core/                     # Componentes centrales
│   │   ├── base_event.py         # Modelo de eventos astrológicos
│   │   ├── constants.py          # Constantes del sistema
│   │   └── location.py           # Manejo de ubicaciones
│   └── utils/                    # Utilidades
│       ├── time_utils.py         # Manejo de tiempo y zonas horarias
│       ├── math_utils.py         # Cálculos matemáticos
│       └── location_utils.py     # Utilidades de geolocalización
├── start_robust.sh               # Script de inicio automático
├── requirements.txt              # Dependencias Python
└── cline_docs/                   # Documentación del proyecto
```

## 🚀 Inicio Rápido

### 1. **Instalación**
```bash
# Clonar el repositorio
git clone https://github.com/AstrologiaMB/astro-calendar-personal-fastapi.git
cd astro-calendar-personal-fastapi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. **Iniciar el Microservicio**
```bash
# Opción recomendada (script automático)
./start_robust.sh

# O manualmente
python app.py
```

### 3. **Verificar Funcionamiento**
```bash
# Health check
curl http://localhost:8004/health

# Información del servicio
curl http://localhost:8004/info
```

El servicio estará disponible en:
- **API**: http://localhost:8004
- **Documentación**: http://localhost:8004/docs
- **ReDoc**: http://localhost:8004/redoc

## 📚 API Endpoints

### **Cálculo Dinámico (Recomendado)**
```http
POST /calculate-personal-calendar-dynamic
Content-Type: application/json

{
  "name": "Usuario Ejemplo",
  "birth_date": "1990-01-15",
  "birth_time": "14:30",
  "location": {
    "latitude": -34.6037,
    "longitude": -58.3816,
    "name": "Buenos Aires",
    "timezone": "America/Argentina/Buenos_Aires"
  },
  "year": 2025
}
```

**Respuesta**: ~200+ eventos astrológicos calculados con interpretaciones

### **Endpoints de Monitoreo**
- `GET /health` - Estado del servicio
- `GET /info` - Información detallada del microservicio
- `GET /` - Información básica y endpoints disponibles

### **Cálculo con Carta Previa (Legacy)**
```http
POST /calculate-personal-calendar
```
Para usar con carta natal pre-calculada.

## 🔧 Configuración Técnica

### **Dependencias Críticas**
- **Python**: 3.8+
- **FastAPI**: 0.115.12+
- **Immanuel**: 1.4.3 (con ephemeris.planet)
- **Swiss Ephemeris**: 2.10.3.2
- **PyEphem**: 9.99

### **Puertos y Servicios**
- **Microservicio**: Puerto 8004
- **Frontend Integration**: Puerto 3000 (sidebar-fastapi)
- **Interpretaciones**: Puerto 8002 (astro_interpretador_rag_fastapi)

### **Variables de Entorno**
```env
# Puerto del servidor (opcional)
PORT=8004

# Configuración de CORS
CORS_ORIGINS=["http://localhost:3000"]

# Nivel de logging
LOG_LEVEL=INFO
```

## 🧮 Tipos de Eventos Calculados

### **1. Tránsitos Astronómicos**
- Conjunciones exactas (orbe ≤ 1°)
- Oposiciones exactas (orbe ≤ 1°)
- Cuadraturas exactas (orbe ≤ 1°)
- Planetas estacionarios (cambios de dirección)

### **2. Tránsitos por Casas**
- **Estado actual** de planetas lentos por casa natal
- **Júpiter**: ~1 año por casa
- **Saturno**: ~2.5 años por casa
- **Urano**: ~7 años por casa
- **Neptuno**: ~14 años por casa
- **Plutón**: ~20 años por casa

### **3. Luna Progresada**
- Conjunciones con planetas natales
- Algoritmo optimizado de alta precisión
- Orbe de 1° para conjunciones

### **4. Profecciones Anuales**
- Sistema tradicional de casas por edad
- Cálculo automático según fecha de nacimiento
- Significados de casas incluidos

### **5. Fases Lunares**
- Lunas nuevas y llenas
- Análisis por casa natal
- Aspectos con planetas natales (orbe 4°)

### **6. Eclipses**
- Eclipses solares y lunares
- Análisis por casa natal
- Aspectos con planetas natales (orbe 4°)

## 🔗 Integración con Ecosistema Astrowellness

### **Frontend React (sidebar-fastapi)**
```typescript
// Llamada desde el frontend
const response = await fetch('http://localhost:8004/calculate-personal-calendar-dynamic', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(birthData)
});

const { events, total_events } = await response.json();
```

### **Servicio de Interpretaciones**
El microservicio se integra automáticamente con el servicio RAG de interpretaciones:
- **URL**: http://localhost:8002/interpretar-eventos
- **Enriquecimiento**: Añade interpretaciones a eventos calculados
- **Fallback**: Devuelve eventos sin interpretar si el servicio no está disponible

### **Flujo de Datos**
```
Frontend → Datos Natales → Calendar API → Cálculos → Interpretaciones → Frontend
```

## 🧪 Testing y Validación

### **Test Rápido**
```bash
# Test básico del endpoint dinámico
curl -X POST http://localhost:8004/calculate-personal-calendar-dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "birth_date": "1990-01-15",
    "birth_time": "14:30",
    "location": {
      "latitude": -34.6037,
      "longitude": -58.3816,
      "name": "Buenos Aires",
      "timezone": "America/Argentina/Buenos_Aires"
    },
    "year": 2025
  }'
```

### **Validación de Precisión**
- Comparación con AstroSeek para tránsitos exactos
- Validación de fases lunares con NASA
- Verificación de eclipses con datos astronómicos oficiales

## 📊 Rendimiento y Optimización

### **Métricas Típicas**
- **Cálculo completo**: ~12-15 segundos
- **Eventos generados**: 200-300 por año
- **Memoria**: ~50MB durante cálculos
- **CPU**: Optimizado para cálculos paralelos

### **Optimizaciones Implementadas**
- Caching de cálculos repetitivos
- Algoritmos paralelos para tránsitos
- Filtrado inteligente de eventos duplicados
- Manejo eficiente de memoria para ephemeris

## 🔍 Solución de Problemas

### **Error: Puerto 8004 en uso**
```bash
# Liberar puerto
kill $(lsof -ti:8004)
./start_robust.sh
```

### **Error: Dependencias faltantes**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### **Error: Timezone inválido**
```bash
# Verificar timezone válido
python -c "from zoneinfo import ZoneInfo; print(ZoneInfo('America/Argentina/Buenos_Aires'))"
```

### **Logs y Debugging**
```bash
# Ver logs en tiempo real
tail -f microservice.log

# Verificar estado de dependencias críticas
python -c "import immanuel; print('Immanuel OK')"
python -c "import swisseph; print('Swiss Ephemeris OK')"
```

## 📚 Documentación Adicional

- **[Características Completas](FEATURES.md)** - Lista detallada de funcionalidades
- **[API Documentation](API_DOCUMENTATION.md)** - Referencia completa de endpoints
- **[Guía de Instalación](SETUP_GUIDE.md)** - Configuración paso a paso
- **[Changelog](CHANGELOG.md)** - Historial de cambios y versiones
- **[Índice de Documentación](DOCUMENTATION_INDEX.md)** - Navegación completa

## 🤝 Contribución

Este microservicio es parte del ecosistema Astrowellness. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### **Áreas de Contribución**
- Nuevos tipos de cálculos astrológicos
- Optimizaciones de rendimiento
- Mejoras en la precisión astronómica
- Documentación y ejemplos
- Tests y validaciones

## 📄 Licencia

Este proyecto es parte del ecosistema Astrowellness desarrollado por AstrologiaMB.

## 🔮 Roadmap

- [ ] **Aspectos Menores**: Sextiles, trígonos, semicuadraturas
- [ ] **Tránsitos Rápidos**: Luna, Mercurio, Venus optimizados
- [ ] **Revoluciones Solares**: Cálculos anuales automatizados
- [ ] **Direcciones Primarias**: Sistema predictivo tradicional
- [ ] **API Versioning**: Versionado de endpoints
- [ ] **Cache Distribuido**: Redis para cálculos compartidos
- [ ] **Métricas Avanzadas**: Monitoring y analytics
- [ ] **Multi-idioma**: Soporte para múltiples idiomas

## 📞 Soporte

Para soporte técnico o preguntas sobre integración:
- **Issues**: GitHub Issues del repositorio
- **Documentación**: Consultar archivos README_*.md
- **Health Check**: Verificar `/health` endpoint
- **Logs**: Revisar logs del microservicio para errores específicos

---

**🌟 Desarrollado con precisión astronómica por el equipo de AstrologiaMB**

*Microservicio de calendario astrológico personal - Versión 2.0.0*
