FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1933

ENV FLASK_APP=run.py

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:1933", "--timeout", "120", "run:app"]
