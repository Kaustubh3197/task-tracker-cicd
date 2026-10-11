# ---- Production image for the Task Tracker ----
FROM python:3.12-slim

# Version number shown on the page and /health (set by the pipeline)
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    DATABASE=/data/tasks.db \
    PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY wsgi.py .

# Don't run as root inside the container
RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser

EXPOSE 8000

# Docker marks the container "unhealthy" if /health stops answering
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ[\"PORT\"]}/health')"

# Hosting platforms like Render tell the app which port to use via $PORT
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 wsgi:app
