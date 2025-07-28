# Problemas de Dependencias - Microservicio RAG

## 🚨 Problema Encontrado

### Error:
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

### Causa:
- Conflicto entre `openai==1.3.7` y `llama-index==0.9.13`
- Python 3.13 con dependencias que esperan versiones más nuevas
- El proyecto original funciona porque tiene un entorno estable congelado

## 🛠️ Soluciones

### ✅ Solución A: Usar entorno original (ACTUAL)
```bash
# Usar el venv del proyecto original que funciona
cd /Users/apple/astro_interpretador_rag
source venv/bin/activate
cd /Users/apple/astro_interpretador_rag_fastapi
python app.py
```

**Pros:**
- Funciona inmediatamente
- Sin riesgo de conflictos
- Usa entorno probado

**Contras:**
- Dependencia del proyecto original
- No es completamente independiente

### 🔄 Solución B: Actualizar versiones (FUTURO)
```bash
# Actualizar requirements.txt con versiones compatibles
pip install openai>=1.40.0 llama-index>=0.10.0
```

### 📦 Solución C: Congelar entorno original (ALTERNATIVA)
```bash
cd /Users/apple/astro_interpretador_rag
source venv/bin/activate
pip freeze > requirements_working.txt
# Usar este archivo en el nuevo proyecto
```

## 🚀 Comandos de Inicio del Sistema

### 1. Iniciar Microservicio RAG (Puerto 8002)
```bash
cd /Users/apple/astro_interpretador_rag
source venv/bin/activate
cd /Users/apple/astro_interpretador_rag_fastapi
python app.py
```

### 2. Iniciar Frontend Next.js (Puerto 3000)
```bash
cd /Users/apple/sidebar-fastapi
npm run dev
```

### 3. Iniciar Microservicio Cálculo (Puerto 8001) - Si es necesario
```bash
cd /Users/apple/calculo-carta-natal-api
source venv/bin/activate
python app.py
```

## 🔗 Flujo Completo

1. **Usuario accede a** `/cartas/tropica`
2. **Calcula carta natal** → Microservicio Cálculo (8001)
3. **Genera interpretaciones** → Microservicio RAG (8002)
4. **Muestra resultado** → Frontend Next.js (3000)

## 📝 Notas Importantes

- **Orden de inicio**: RAG primero, luego Frontend
- **Dependencias**: El microservicio RAG depende del entorno del proyecto original
- **Puertos**: 8001 (Cálculo), 8002 (RAG), 3000 (Frontend)
- **Cache**: Las interpretaciones se cachean en Prisma por 30 días

## 🎯 TODO Futuro

- [ ] Implementar Solución B con versiones actualizadas
- [ ] Crear entorno completamente independiente
- [ ] Dockerizar microservicios para evitar conflictos
- [ ] Crear script de inicio automatizado

## 🔄 Estado Actual del Problema

### Problema Persistente:
- Incluso usando el entorno original, hay conflictos de versiones
- El error `Client.__init__() got an unexpected keyword argument 'proxies'` persiste
- Indica incompatibilidad entre httpx y openai en el contexto de llama-index

### Análisis Técnico:
- `httpx==0.28.1` en el entorno original
- `openai==1.3.7` y `llama-index==0.9.13`
- El problema surge al crear embeddings con OpenAI

### Solución Temporal:
Crear un microservicio simplificado sin RAG que use interpretaciones estáticas mientras se resuelve el conflicto de dependencias.

---
**Fecha**: 2025-06-09  
**Estado**: Problema de dependencias persistente - Implementando solución temporal
