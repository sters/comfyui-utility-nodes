.PHONY: help sync lint fmt fmt-check typecheck test check fix clean integration integration-up integration-down integration-logs

help:
	@echo "Targets:"
	@echo "  sync       - install dependencies via uv"
	@echo "  lint       - ruff check"
	@echo "  fmt        - ruff format (write)"
	@echo "  fmt-check  - ruff format --check"
	@echo "  typecheck  - mypy"
	@echo "  test       - pytest"
	@echo "  check      - lint + fmt-check + typecheck + test"
	@echo "  fix        - ruff check --fix + ruff format"
	@echo "  integration - run integration check against a running ComfyUI (see tests/integration/README.md)"
	@echo "  clean      - remove caches"

sync:
	uv sync

lint:
	uv run ruff check .

fmt:
	uv run ruff format .

fmt-check:
	uv run ruff format --check .

typecheck:
	uv run mypy

test:
	uv run pytest

check: lint fmt-check typecheck test

fix:
	uv run ruff check --fix .
	uv run ruff format .

COMPOSE := docker compose -f tests/integration/docker-compose.yml

integration-up:
	$(COMPOSE) up -d --build --wait

integration-down:
	$(COMPOSE) down

integration-logs:
	$(COMPOSE) logs --tail=200

integration: integration-up
	uv run python -m tests.integration.run
	$(COMPOSE) down

clean:
	rm -rf .ruff_cache .mypy_cache .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
