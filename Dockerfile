FROM python:3.11 AS base_bare

LABEL NAME=pipelines
LABEL VERSION=1.0.0

WORKDIR /app/

# Install poetry, do this before copying files for caching purposes.
RUN pip install --upgrade pip
RUN pip install poetry==1.8.2

# Copy pyproject.toml, poetry.lock and README.md files.
COPY pyproject.toml poetry.lock README.md ./
COPY pipelines/__init__.py pipelines/__init__.py

# Install dependencies.
RUN poetry config virtualenvs.create false && poetry install

ENTRYPOINT [ "bash" ]

FROM base_bare AS base

# Copy all other files here to optimize caching.
COPY ./ ./

FROM base_bare AS test

# Dependencies for pre-commit.
RUN apt-get update \
    && apt-get install git build-essential shellcheck -y \
    && apt-get clean
RUN poetry install --with dev,test
COPY .pre-commit-config.yaml .pre-commit-config.yaml

# Install pre-commit hooks.
RUN git init . && pre-commit install-hooks
RUN git config --global --add safe.directory /app
