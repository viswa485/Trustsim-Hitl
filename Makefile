.PHONY: install test lint run
install:
	python -m pip install -e ".[dev]"
test:
	pytest
lint:
	ruff check .
run:
	trustsim run --episodes 100 --seed 2026 --output-dir results/local-run
