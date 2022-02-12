#!/bin/bash

set -e

poetry install

if [ $1 == 'true' ]; then
    poetry run flake8
fi

if [ $2 == 'true' ]; then
    poetry run pytest ./tests
fi

if [ $3 == 'true' ]; then
    poetry run coverage run -m pytest ./tests
    poetry run coverage report --fail-under 80 -m
fi
