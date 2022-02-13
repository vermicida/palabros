FROM python:3.8-slim

ARG POETRY_VERSION

RUN pip install --no-cache-dir poetry==$POETRY_VERSION \
                               "semver>=2.13,<3" \
                               "requests>=2.26"

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
