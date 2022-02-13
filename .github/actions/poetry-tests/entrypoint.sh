#!/bin/bash

set -e

poetry install

if [ $1 == 'true' ]; then
    echo -e '\n-->> Running linting analysis\n'
    poetry run flake8
fi

if [ $2 == 'true' ]; then
    echo -e '\n-->> Running unit testing\n'
    poetry run pytest ./tests
fi

if [ $3 == 'true' ]; then
    echo -e '\n-->> Running coverage testing\n'
    poetry run coverage run -m pytest ./tests
    poetry run coverage report --fail-under 80 -m
fi
