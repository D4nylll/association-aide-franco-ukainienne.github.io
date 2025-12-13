#docker/backend/Dockerfile

# ===== Stage 1: Build environment =====
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent .pyc files and set buffer off for logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY my_shop/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY my_shop /app

# Collect static files
# RUN python manage.py collectstatic --noinput || true

# Run server
CMD ["gunicorn", "my_shop.wsgi:application", "--bind", "0.0.0.0:8000"]