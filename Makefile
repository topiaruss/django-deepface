.PHONY: install test lint format clean build upload dev update-badge prepare-release

# Development setup
install:
	uv sync

dev: install
	uv run pre-commit install

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov-report=html

# Code quality
lint:
	uv run ruff check .

format:
	uv run ruff format .

check: format lint

# Building and uploading
build: update-badge
	uv build

upload:
	uv publish

# Utilities
update-badge:
	uv run python scripts/update_badge.py

prepare-release:
	uv run python scripts/prepare_release.py

# Cleanup
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
