FROM python:3.13-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web ./web
COPY shared ./shared

ENV DATABASE_URL="sqlite:///./glossary.db"

EXPOSE 8000

CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]