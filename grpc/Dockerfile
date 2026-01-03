FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grpc ./grpc
COPY shared ./shared

VOLUME ["/app/db"]

EXPOSE 50051

ENV PYTHONPATH=/app

CMD ["python", "grpc/server.py"]