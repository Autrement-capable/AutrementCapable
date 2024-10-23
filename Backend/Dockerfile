FROM python:3.10.15-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ARG DEBUG=false

ENV DEBUG=${DEBUG}

# Expose ports for the app and debug mode
EXPOSE ${PORT}
# EXPOSE ${DEBUG_PORT}
# hardcoding the debug port to 5678 because it does not accecpt it otherwise
EXPOSE 5678

# Check the DEBUG environment variable to run the app in debug mode or normal mode
CMD if [ "$DEBUG" = "true" ]; then \
        python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py; \
    else \
        python app.py; \
    fi