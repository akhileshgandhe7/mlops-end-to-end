.PHONY: whoami setup test lint data train evaluate serve

whoami:    ## fail unless AWS points at the personal account (EXPECTED_AWS_ACCOUNT from .envrc)
	@test -n "$(EXPECTED_AWS_ACCOUNT)" || { echo "STOP: EXPECTED_AWS_ACCOUNT unset - is direnv loaded?"; exit 1; }
	@acct=$$(aws sts get-caller-identity --query Account --output text) && \
	if [ "$$acct" = "$(EXPECTED_AWS_ACCOUNT)" ]; then echo "OK: personal account $$acct ($(AWS_PROFILE))"; \
	else echo "STOP: AWS points at account $$acct, expected $(EXPECTED_AWS_ACCOUNT)"; exit 1; fi

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
