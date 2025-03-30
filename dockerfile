# Use Python Alpine as the base image for a smaller footprint
FROM python:3.9-alpine as builder

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    make

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Second stage - final image
FROM python:3.9-alpine

# Install runtime dependencies
RUN apk add --no-cache libstdc++ libffi openssl

# Create a non-root user to run the app
RUN adduser -D django
USER django

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=django:django . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=broadcast_project.settings

# Expose the port
EXPOSE 8000

# Run Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "broadcast_project.asgi:application"]