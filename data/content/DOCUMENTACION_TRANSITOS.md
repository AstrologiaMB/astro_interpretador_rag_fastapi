# Documentación de Gestión de Contenido de Tránsitos

Esta guía explica cómo se estructura la base de datos de interpretaciones astrológicas, cómo modificar textos y la arquitectura híbrida del sistema.

## 🏗 Arquitectura del Sistema (Híbrida)

El interpretador utiliza dos motores distintos según el tipo de consulta, optimizando precisión vs. creatividad.

### 1. Sistema de Cartas Natales (RAG / Inteligencia Artificial)
*   **Endpoints:** `/interpretar` (Natal Tropical y Dracónica).
*   **Funcionamiento:** Utiliza **RAG (Retrieval-Augmented Generation)**. Lee los archivos Markdown originales, busca similitud semántica y un LLM (OpenAI/Anthropic) redacta una interpretación única y fluida.
*   **Fuente de Datos:** Archivos MD en `data/` y `data/draco/`.
*   **Objetivo:** Profundidad psicológica y narrativa personalizada.

### 2. Sistema de Calendario Personal (JSON / Determinista)
*   **Endpoint:** `/interpretar-eventos` (Tránsitos Diarios).
*   **Funcionamiento:** Utiliza un motor **Determinista (JSON)**. Busca una llave exacta en la base de datos pre-compilada. Si la encuentra (cobertura actual 100%), devuelve el texto *verbatim*.
*   **Fuente de Datos:** `astro_interpretador_rag_fastapi/data/transitos.json`.
*   **Objetivo:** Velocidad extrema, precisión predictiva y consistencia total (mismo evento = misma descripción).

---

## 🛠 Flujo de Trabajo para Tránsitos

El sistema de tránsitos sigue el flujo: **Fuente de Verdad (Markdown)** -> **Compilación (Script)** -> **Base de Datos (JSON)**.

### Archivos Clave

1.  **Fuente de Verdad (¡EDITAR AQUÍ!)**: 
    `astro_interpretador_rag_fastapi/data/content/source_transits.md`
    *   Este es el archivo maestro. Contiene todas las descripciones en formato Markdown.
    *   Formato de encabezado: `#### Planeta en Tránsito Aspecto a Planeta Natal`

2.  **Script de Compilación**:
    `astro_interpretador_rag_fastapi/data/parse_interpretations.py`
    *   Lee `source_transits.md`.
    *   Normaliza los títulos y genera `transitos.json`.

3.  **Base de Datos (Producción)**:
    `astro_interpretador_rag_fastapi/data/transitos.json`
    *   Leído por la API en tiempo real. **NO EDITAR MANUALMENTE** (se sobrescribe).

---

## ✍️ Cómo Modificar o Corregir Textos

Si deseas ajustar una interpretación de tránsito:

1.  **Editar el Markdown**:
    Abre `/Users/apple/astrochat/astro_interpretador_rag_fastapi/data/content/source_transits.md`.

2.  **Buscar el Evento**:
    Usa `Ctrl+F` para buscar el título (ej: "Júpiter en tránsito conjunción a Luna").

3.  **Modificar el Texto**:
    Edita el párrafo.
    *   **Placeholders:** Puedes usar `{fecha}` para que el sistema inserte la fecha del evento.
    *   **Limpieza:** Asegúrate de NO dejar comentarios HTML (ej: `<!-- GENERATED -->`) ya que aparecerán en el texto final.

4.  **Guardar y Re-compilar**:
    Ejecuta el script para actualizar el JSON:
    ```bash
    /Users/apple/astrochat/astro_interpretador_rag_fastapi/venv/bin/python /Users/apple/astrochat/astro_interpretador_rag_fastapi/data/parse_interpretations.py
    ```
    *Debe decir: `Extracted X items to transitos.json`.*

5.  **Reiniciar Servidor** (Opcional):
    ```bash
    ./stop_astro.sh && ./start_astro.sh
    ```

---

## 🧪 Auditoría y Verificación

Si dudas de la cobertura o quieres ver qué texto está recibiendo un usuario:

1.  **Generar CSV de Auditoría**:
    Usa el script `generate_audit_csv.py` (en la raíz).
    ```bash
    /Users/apple/astrochat/astro-calendar-personal-fastapi/venv/bin/python generate_audit_csv.py
    ```
    Esto creará un archivo CSV con todos los eventos del año 2026 y sus textos actuales.

2.  **Script de Cobertura**:
    Usa `audit_specific_user.py` para verificar porcentaje de cobertura matemática.

---

## 📜 Historial de Cambios (Enero 2026)

*   **Auditoría de Cobertura:** Se detectaron 260 faltantes.
*   **Generación Masiva:** Se completaron usando IA con estilo "Clásico/Predictivo".
*   **Fusión:** Se integraron en `source_transits.md`.
*   **Limpieza:** Se eliminaron artefactos HTML corruptos.
*   **Estado Actual:** 100% de Cobertura (611 eventos únicos).
