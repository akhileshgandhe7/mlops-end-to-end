.PHONY: setup test lint data train evaluate serve

setup:     ## create .venv and install everything
	uv sync --all-extras

test:
	uv run pytest -q

lint:
	uv run ruff check .

data:      ## phase 1: fake queries -> data/raw/
	uv run python -m query_parser.generate_data

train:     ## phase 1: train + log to MLflow -> models/
	uv run python -m query_parser.train

evaluate:  ## phase 1: golden-set gate
	uv run python -m query_parser.evaluate

serve:     ## phase 2: FastAPI locally
	uv run uvicorn query_parser.app:app --reload
