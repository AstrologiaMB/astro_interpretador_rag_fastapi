# Migración a Baseten (Kimi-K2.5)

Este documento describe los cambios realizados para migrar el servicio de usar Anthropic (Claude) a Baseten con el modelo Kimi-K2.5.

## Cambios Realizados

### 1. Archivo: `interpretador_refactored.py`

#### Nuevo: Clase `BasetenLLM`
- Implementa un wrapper compatible con `llama-index` que usa el cliente OpenAI para conectarse a Baseten
- Baseten tiene una API compatible con OpenAI, por lo que podemos usar el cliente oficial de OpenAI
- Endpoint: `https://inference.baseten.co/v1`
- Modelo: `moonshotai/Kimi-K2.5`

#### Cambios en `__init__`:
- Reemplaza `ANTHROPIC_API_KEY` por `BASETEN_API_KEY`
- Lanza error si no se encuentra la API key de Baseten

#### Cambios en `_setup_llm_and_embeddings`:
- Usa `BasetenLLM` en lugar de `Anthropic` para el RAG y el escritor narrativo
- Dos instancias de BasetenLLM:
  - **RAG**: `temperature=0.0`, `max_tokens=4096` (respuestas consistentes)
  - **Escritor**: `temperature=0.7`, `max_tokens=16000` (creatividad para narrativa)

### 2. Archivo: `.env.example`

Agregada la variable:
```
BASETEN_API_KEY=your-baseten-api-key-here
```

### 3. Archivo: `requirements.txt`

Eliminadas las dependencias de Anthropic:
- `anthropic>=0.18.0`
- `llama-index-llms-anthropic>=0.1.0`

La dependencia `openai` ya está incluida y se usa para conectarse a Baseten.

## Configuración

### 1. Obtener API Key de Baseten

1. Ve a [baseten.co](https://baseten.co) e inicia sesión
2. Navega a tu dashboard y obtén tu API key
3. Asegúrate de tener acceso al modelo `moonshotai/Kimi-K2.5`

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Baseten (Kimi-K2.5)
BASETEN_API_KEY=tu-api-key-de-baseten

# OpenAI (para embeddings - requerido)
OPENAI_API_KEY=sk-tu-api-key-de-openai

# CORS y Puerto
CORS_ORIGINS=*
PORT=8002
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Nota: Si tenías instaladas las dependencias de Anthropic, puedes desinstalarlas:
```bash
pip uninstall anthropic llama-index-llms-anthropic
```

## Ejecución

```bash
python app.py
```

O usando uvicorn directamente:

```bash
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```

## Verificación

El servicio iniciará y mostrará:

```
✅ InterpretadorRAG refactorizado inicializado correctamente
🔧 Feature Flag - RAGs Separados: ACTIVADO
```

Si hay problemas con la API key de Baseten, verás:

```
❌ Error al inicializar Interpretador RAG: BASETEN_API_KEY no encontrada en variables de entorno
```

## Notas Técnicas

### Compatibilidad con llama-index

La clase `BasetenLLM` implementa la interfaz `LLM` de llama-index con los siguientes métodos:
- `complete(prompt)` - Método sincrónico principal
- `acomplete(prompt)` - Método asíncrono
- `chat(messages)` - Para conversaciones multi-mensaje
- `achat(messages)` - Versión asíncrona de chat

### Embeddings

Los embeddings siguen usando OpenAI (`OpenAIEmbedding`) ya que Baseten no proporciona servicio de embeddings. Esto es normal y no afecta el funcionamiento del RAG.

### Diferencias con Anthropic

| Característica | Anthropic (Claude) | Baseten (Kimi-K2.5) |
|---------------|-------------------|---------------------|
| API Key | `ANTHROPIC_API_KEY` | `BASETEN_API_KEY` |
| Endpoint | api.anthropic.com | inference.baseten.co/v1 |
| Cliente | anthropic | openai (compatible) |
| Modelos RAG | claude-haiku | moonshotai/Kimi-K2.5 |
| Modelos Escritor | claude-sonnet | moonshotai/Kimi-K2.5 |

## Troubleshooting

### Error: "BASETEN_API_KEY no encontrada"
Asegúrate de que el archivo `.env` existe y tiene la variable `BASETEN_API_KEY` definida.

### Error de conexión a Baseten
Verifica que tu API key sea válida y tengas acceso al modelo `moonshotai/Kimi-K2.5`.

### Error en embeddings
Asegúrate de que `OPENAI_API_KEY` esté configurada correctamente, ya que los embeddings siguen usando OpenAI.
