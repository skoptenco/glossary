FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grpc .
COPY shared ./shared

VOLUME ["/app/db"]

EXPOSE 50051

CMD ["python", "server.py"]