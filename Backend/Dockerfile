FROM python:3.10.15-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ARG DEBUG="true"
ARG DEBUG_PORT=5678

ENV DEBUG=${DEBUG}
ENV HOST="0.0.0.0"
Env DEBUG_PORT=${DEBUG_PORT}

ENV DEBUG=${DEBUG}
ENV PORT=${PORT}
ENV DEBUG_PORT=${DEBUG_PORT}
ENV HOST=${HOST}

# Expose ports for the app and debug mode
EXPOSE ${PORT}
# EXPOSE ${DEBUG_PORT}
# hardcoding the debug port to 5678 because it does not accecpt it otherwise
EXPOSE ${DEBUG_PORT}

# Check the DEBUG environment variable to run the app in debug mode or normal mode
CMD if [ "$DEBUG" = "true" ]; then \
       python -m debugpy --listen ${HOST}:${DEBUG_PORT} --wait-for-client -m uvicorn app:app --host \
       ${HOST} --port ${PORT} --reload; \
    else \
       uvicorn app:app --host ${HOST} --port ${PORT} --reload; \
    fi