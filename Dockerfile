# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install dependencies first for better layer caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy the application
COPY . .

# Run as a non-root user
RUN useradd --create-home appuser && chown -R appuser /usr/src/app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]
