FROM python:3.10.15-slim

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG DEBUG="true"
ARG DEBUG_PORT=5678

ENV DEBUG=${DEBUG}
ENV HOST="0.0.0.0"
ENV DEBUG_PORT=${DEBUG_PORT}
ENV PORT=5000

# Expose ports for the app and debug mode
EXPOSE ${PORT}
EXPOSE ${DEBUG_PORT}

# Check the DEBUG environment variable to run the app in debug mode or normal mode
CMD if [ "$DEBUG" = "true" ]; then \
       python -m debugpy --listen ${HOST}:${DEBUG_PORT} --wait-for-client -m uvicorn app:app --host \
       ${HOST} --port ${PORT} --reload; \
    else \
       uvicorn app:app --host ${HOST} --port ${PORT} --reload; \
    fi
