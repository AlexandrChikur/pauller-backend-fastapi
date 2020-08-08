FROM python:3.8.1-slim

ENV \
  #python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  #poetry
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.0.5


RUN apt-get update \
    && apt-get install netcat -y \
    && python -m pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry --version

WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/
RUN mkdir -p /app/docker

RUN poetry install

COPY ./docker/entrypoint.sh /docker/entrypoint.sh
ENTRYPOINT ["/docker/entrypoint.sh"]

COPY . /app

