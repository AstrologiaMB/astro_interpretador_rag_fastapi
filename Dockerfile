# Dockerfile for astro_interpretador_rag_fastapi - Railway deployment
FROM python:3.11-slim

ARG COMMIT_SHA
ENV COMMIT_SHA=$COMMIT_SHA

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application (including .md files for RAG)
COPY . .

# Expose port for Fly.io
EXPOSE 8002

# CRITICAL: Uvicorn with longer timeout for OpenAI calls and Fly.io compatibility
CMD uvicorn app:app \
    --host 0.0.0.0 \
    --port 8002 \
    --timeout-keep-alive 300 \
    --access-log \
    --log-level info
