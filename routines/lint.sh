poetry run black src
poetry run isort src
poetry run ruff check --fix src
