# Deploy a Fly.io

## Paso 1: Subir la branch y crear Pull Request

```bash
# En tu máquina local (si no lo has hecho ya)
git push -u origin migrate-to-baseten-kimi

# Luego crea el PR en GitHub y márgalo a main
git checkout main
git pull origin main
```

## Paso 2: Configurar Secrets en Fly.io

```bash
# Verificar que estás en el app correcto
fly apps list

# Configurar las variables de entorno en fly.io
# Necesitas configurar BASETEN_API_KEY (nueva) y OPENAI_API_KEY (existente)

# Primero, ver los secrets actuales
fly secrets list

# Si ANTHROPIC_API_KEY existe, puedes eliminarlo (ya no se usa)
fly secrets unset ANTHROPIC_API_KEY

# Configurar la nueva API key de Baseten
fly secrets set BASETEN_API_KEY="rGCPsB3m.UXbDXIKtDiNDn0qTxuQognv3LDaeMykw"

# Verificar que OPENAI_API_KEY está configurado
fly secrets set OPENAI_API_KEY="sk-tu-openai-key-aqui"

# Si tienes CORS_ORIGINS configurado, mantenlo
# Si no, configúralo:
fly secrets set CORS_ORIGINS="*"
```

## Paso 3: Deploy

```bash
# Hacer deploy desde la branch main (después de mergear el PR)
git checkout main
git pull origin main

# Deploy a fly.io
fly deploy
```

## Paso 4: Verificar el deploy

```bash
# Ver logs
fly logs

# Verificar health check
fly status

# Hacer una petición de prueba
curl https://astro-interpretador-rag-fastapi.fly.dev/health
```

## Cambios en Variables de Entorno

| Variable | Antes | Después |
|----------|-------|---------|
| `ANTHROPIC_API_KEY` | ✅ Requerida | ❌ Eliminada |
| `BASETEN_API_KEY` | No existía | ✅ Requerida |
| `OPENAI_API_KEY` | ✅ Requerida (embeddings) | ✅ Requerida (embeddings) |

## Archivos Modificados

- `interpretador_refactored.py` - Nueva clase BasetenLLM
- `requirements.txt` - Eliminadas dependencias de anthropic
- `.env.example` - Nueva variable BASETEN_API_KEY
- `prompts.py` - Actualizado comentario
- Scripts de prueba actualizados

## Rollback (si es necesario)

Si algo sale mal, puedes volver a la versión anterior:

```bash
# Ver releases anteriores
fly releases list

# Hacer rollback a una versión anterior
fly deploy --image flyio/astro-interpretador-rag-fastapi:<sha-anterior>
```

## Notas Importantes

1. **Tiempo de inicio**: La primera vez que se inicie con Kimi-K2.5 puede tardar un poco más mientras se indexan los documentos.

2. **Memoria**: El servicio usa ~1GB de RAM durante la indexación inicial. El `fly.toml` ya tiene configurado `memory = '1024mb'`.

3. **Endpoints**: Los endpoints no cambian:
   - `POST /interpretar` - Interpretación completa
   - `POST /interpretar-eventos` - Interpretación de eventos de calendario
   - `GET /health` - Health check
