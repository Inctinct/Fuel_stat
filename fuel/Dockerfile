FROM python:3.11

ENV PYTHONBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD=25Mdd2515!
ENV DJANGO_SETTINGS_MODULE=fuel.settings

WORKDIR /app

COPY poetry.lock pyproject.toml /app

RUN pip3 install poetry

RUN poetry install
