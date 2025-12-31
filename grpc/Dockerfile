FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/db

COPY --from=builder /install /usr/local

COPY glossary.proto .
COPY glossary_pb2.py .
COPY glossary_pb2_grpc.py .

COPY server.py .
COPY storage.py .
COPY models.py .

VOLUME ["/app/db"]

EXPOSE 50051

CMD ["python", "server.py"]