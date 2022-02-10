FROM python:slim AS base

RUN \
    pip install poetry==1.1.11 \
                "semver>=2.13,<3" \
                "requests>=2.26"

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
