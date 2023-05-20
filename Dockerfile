#Подготовка
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Финальный этап
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get install ffmpeg


COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

COPY requirements.txt .

RUN pip install --no-cache /wheels/*

COPY app app
COPY alembic alembic
COPY alembic.ini alembic.ini

CMD ["uvicorn", "__main__:app", "--host", "0.0.0.0", "--port", "8080"]
