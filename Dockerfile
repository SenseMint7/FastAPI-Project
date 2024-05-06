FROM python:3.11-slim as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN mkdir -p /fastapi-project

COPY . /fastapi-project

WORKDIR /fastapi-project

RUN apt-get update \
 && apt-get install -y build-essential \
 && pip install --upgrade pip \
 && pip install poetry \
 && poetry install --without test \
 && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim as runtime

COPY --from=builder /fastapi-project /fastapi-project

WORKDIR /fastapi-project

RUN apt-get update \
 && apt-get install make

ENV VIRTUAL_ENV=/fastapi-project/.venv \
    PATH="/fastapi-project/.venv/bin:$PATH"
