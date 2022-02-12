FROM python:3.8-slim

ARG POETRY_VERSION

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
