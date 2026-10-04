# Production image for the Humana Apparels site (Django + gunicorn).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# requirements.txt is hash-pinned (poetry export); gunicorn is the
# container's app server only, so it is installed separately.
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install gunicorn==23.0.0

COPY . .
RUN chmod +x docker/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-"]
