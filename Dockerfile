# Dockerfile for astro_interpretador_rag_fastapi - Railway deployment
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application (including .md files for RAG)
COPY . .

# Expose port (Railway ignores this but good practice)
EXPOSE 8080

# CRITICAL: Uvicorn with longer timeout for OpenAI calls and Railway compatibility
CMD uvicorn app:app \
    --host 0.0.0.0 \
    --port $PORT \
    --timeout-keep-alive 300 \
    --access-log \
    --log-level info
