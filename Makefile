.PHONY: test
test:
	poetry run pytest ./tests

.PHONY: coverage
coverage:
	poetry run coverage run -m pytest ./tests
	poetry run coverage report --fail-under 80 -m

.PHONY: lint
lint:
	poetry run flake8
