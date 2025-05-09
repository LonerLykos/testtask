FROM python:3.12-alpine

LABEL maintainer='Some Dev'

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libffi-dev \
    shared-mime-info \
    curl

RUN mkdir /app
WORKDIR /app

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH


COPY pyproject.toml /app/
COPY backend/ /app/


RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install