FROM python:3.10.15-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ARG PORT=5000

EXPOSE $PORT

CMD ["python", "app.py"]