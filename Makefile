.PHONY: test-all test-all-first test-specific clean db-migrate init lint format check

# Test targets
test-all:
	python -m pytest django_deepface/tests/ --cov=django_deepface --cov-report=term-missing -v

test-all-first:
	python -m pytest django_deepface/tests/ --cov=django_deepface --cov-report=term-missing -v --exitfirst

test-specific:
	python -m pytest $(filter-out $@,$(MAKECMDGOALS)) --cov=django_deepface --cov-report=term-missing -v

# Linting and formatting targets
lint:
	ruff check .

format:
	ruff format .

check: lint format

# Database targets
db-migrate:
	python manage.py migrate

# Cleanup targets
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".DS_Store" -delete

# Initialization target
init: clean
	uv pip install -e .
	uv pip install pytest pytest-django pytest-cov
	make db-migrate
