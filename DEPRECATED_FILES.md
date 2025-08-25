# ❌ Archivos Deprecated - NO USAR

**Fecha de deprecación**: 26 de junio de 2025  
**Motivo**: Actualización de documentación y consolidación de archivos

## 🚫 Archivos de Código Obsoletos

### `main.py`
- **Estado**: DEPRECATED
- **Motivo**: Versión standalone obsoleta, reemplazada por arquitectura FastAPI
- **Usar en su lugar**: `app.py`
- **Descripción**: Versión original que funcionaba como script independiente con input manual. Contiene lógica de aspectos complejos que fue migrada a `interpretador_refactored.py`

### `app_simple.py`
- **Estado**: DEPRECATED
- **Motivo**: Versión simplificada sin funcionalidades completas
- **Usar en su lugar**: `app.py`
- **Descripción**: Versión reducida del microservicio FastAPI sin aspectos complejos ni funcionalidades avanzadas

### `interpretador.py`
- **Estado**: DEPRECATED
- **Motivo**: Versión original sin refactorizar
- **Usar en su lugar**: `interpretador_refactored.py`
- **Descripción**: Primera implementación del sistema RAG, sin optimizaciones ni aspectos complejos

## 📦 Archivos de Dependencias Obsoletos

### `requirements_fixed.txt`
- **Estado**: DEPRECATED
- **Motivo**: Versión alternativa con dependencias específicas
- **Usar en su lugar**: `requirements.txt`
- **Descripción**: Versión con dependencias "fijas" para resolver problemas específicos, ya no necesaria

### `requirements_simple.txt`
- **Estado**: DEPRECATED
- **Motivo**: Versión reducida de dependencias
- **Usar en su lugar**: `requirements.txt`
- **Descripción**: Versión minimalista sin todas las funcionalidades

## 📖 Archivos de Documentación Obsoletos

### `aspectos_complejos_definiciones.md`
- **Estado**: DEPRECATED
- **Motivo**: Documentación de planificación ya implementada
- **Usar en su lugar**: Ver `README.md` sección "Aspectos Complejos"
- **Descripción**: Documento de planificación para implementar aspectos complejos. La funcionalidad ya está implementada en `interpretador_refactored.py`

## 🔄 Archivos de Respaldo en `/data`

### Archivos de Títulos Backup
- `Títulos Numerados tropico backup.md`
- `Títulos Numerados tropico luego del backup.md`
- `Títulos Numerados tropico viejos.md`
- **Estado**: DEPRECATED
- **Motivo**: Versiones de respaldo de estandarización
- **Usar en su lugar**: `Títulos Numerados tropico.md`

### Archivos de Interpretaciones Backup
- `interpretaciones_backup_20250605_170151.md`
- `interpretaciones_corrupted.md`
- `interpretaciones_old.txt`
- **Estado**: DEPRECATED
- **Motivo**: Versiones de respaldo y archivos corruptos
- **Usar en su lugar**: `interpretaciones.md`

### Archivos de Testing y Output (Cartas de Prueba)
- `carta_natal_tropical_Lmyahora_Buenos_Aires_26-12-1964*.json/txt`
- `carta_natal_tropical_Lmyahora_Buenos_Aires_26-12-1964copy*.json/txt`
- `carta_natal_tropical_Maria_Blaquier_Buenos_Aires_3-11-1967*.json/txt/csv`
- **Estado**: DEPRECATED (archivos de testing)
- **Motivo**: Outputs de pruebas de desarrollo, no parte del sistema
- **Descripción**: Resultados de interpretaciones de cartas de prueba durante desarrollo

### Archivos CSV de Testing
- `eventos_con_interpretacion_openai.csv`
- `eventos.csv`
- **Estado**: DEPRECATED (archivos de testing)
- **Motivo**: CSVs de prueba del sistema anterior
- **Descripción**: Datos de testing del sistema standalone obsoleto

### Archivos del Sistema
- `.DS_Store`
- **Estado**: DEPRECATED (archivo del sistema)
- **Motivo**: Archivo del sistema macOS, no parte del proyecto
- **Acción**: Debería estar en .gitignore

## ⚠️ Archivos de Problemas Resueltos

### `DEPENDENCY_ISSUES.md`
- **Estado**: DEPRECATED (pero mantener para referencia)
- **Motivo**: Problemas de dependencias ya resueltos
- **Descripción**: Documentación de problemas de dependencias que ya fueron solucionados

## 🎯 Archivos Principales a Usar

### ✅ Código Principal
```
app.py                          # 🎯 Archivo principal FastAPI
interpretador_refactored.py     # 🧠 Lógica RAG refactorizada
requirements.txt                # 📦 Dependencias principales
```

### ✅ Datos y Configuración
```
/data/1-19 *.md                 # 📚 Base de conocimiento astrológico
/data/Títulos Numerados tropico.md  # 📋 Índice de títulos
/data/interpretaciones.md       # 📖 Interpretaciones consolidadas
```

### ✅ Documentación Actualizada
```
README.md                       # 📖 Documentación principal
DEPRECATED_FILES.md             # ❌ Este archivo
/cline_docs/                    # 📝 Documentación de memoria actualizada
```

## 🔧 Comandos de Limpieza (Futuro)

### Mover archivos deprecated a carpeta separada
```bash
# Crear carpetas deprecated
mkdir deprecated
mkdir deprecated/data_backups
mkdir deprecated/data_testing

# Mover archivos de código obsoletos
mv main.py deprecated/
mv app_simple.py deprecated/
mv interpretador.py deprecated/
mv requirements_fixed.txt deprecated/
mv requirements_simple.txt deprecated/
mv aspectos_complejos_definiciones.md deprecated/

# Mover backups de data
mv data/*backup* deprecated/data_backups/
mv data/*old* deprecated/data_backups/
mv data/*corrupted* deprecated/data_backups/

# Mover archivos de testing de data
mv data/carta_natal_tropical_Lmyahora_* deprecated/data_testing/
mv data/carta_natal_tropical_Maria_Blaquier_* deprecated/data_testing/
mv data/eventos*.csv deprecated/data_testing/

# Limpiar archivos del sistema
rm data/.DS_Store
```

### Actualizar .gitignore
```bash
# Agregar al .gitignore para evitar futuros .DS_Store
echo ".DS_Store" >> .gitignore
echo "data/.DS_Store" >> .gitignore
echo "data/*_interpretada_*" >> .gitignore
echo "data/carta_natal_tropical_*" >> .gitignore
```

## 📋 Checklist de Verificación

Antes de usar cualquier archivo, verificar:

- [ ] ¿Está en la lista de archivos principales? ✅ Usar
- [ ] ¿Está en este archivo DEPRECATED? ❌ NO usar
- [ ] ¿Tiene "backup", "old", "simple" en el nombre? ❌ Probablemente deprecated
- [ ] ¿Es la versión más reciente? ✅ Verificar fecha de modificación

## 🔄 Reversión de Emergencia

Si algo falla después de esta reorganización:

```bash
# Volver al commit anterior
git reset --hard b00898d

# O revertir este commit específico
git revert [commit-hash-de-esta-actualizacion]
```

---

**📝 Nota**: Este archivo documenta el estado al 26 de junio de 2025. Los archivos deprecated se mantienen en el repositorio por seguridad, pero NO deben usarse para desarrollo futuro.

**🎯 Regla de oro**: Si tienes dudas sobre qué archivo usar, consulta `README.md` o este archivo.
