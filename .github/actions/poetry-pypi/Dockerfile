FROM python:slim AS base

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM base

RUN \
    pip install poetry==1.1.11 \
                "semver>=2.13,<3" \
                "requests>=2.26"

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
