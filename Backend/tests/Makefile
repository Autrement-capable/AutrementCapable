# Help command
help:
	@echo "Available commands:"
	@echo "  setup         - Install dependencies and set up the environment"
	@echo "  run-dev       - Run the API server in development mode"
	@echo "  run-docker    - Run the API server using Docker"
	@echo "  test          - Run all tests with Docker"
	@echo "  test-endpoint - Run only endpoint tests"
	@echo "  test-func     - Run only functionality tests"
	@echo "  coverage      - Generate and view test coverage report"
	@echo "  clean         - Clean up temporary files and caches"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code"

# Setup command
setup:
	pip install -r requirements.txt
	pip install -r tests/requirements.test.txt

# Development server
run-dev:
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Docker server
run-docker:
	docker-compose up --build

# Test commands
test:
	@echo "Running all tests..."
	@chmod +x tests/run_tests.sh
	@./tests/run_tests.sh

test-endpoint:
	@echo "Running endpoint tests..."
	@chmod +x tests/run_tests.sh
	@./tests/run_tests.sh endpoint -v

test-func:
	@echo "Running functionality tests..."
	@chmod +x tests/run_tests.sh
	@./tests/run_tests.sh functionality -v

# Coverage report
coverage:
	@echo "Generating coverage report..."
	@chmod +x tests/run_tests.sh
	@./tests/run_tests.sh
	@echo "Opening coverage report in browser..."
	@python -m webbrowser -t "file://$(shell pwd)/coverage/index.html"

# Clean up
clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@rm -rf coverage/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@echo "Done cleaning up."

# Linting and formatting
lint:
	@echo "Running linting checks..."
	flake8 .
	isort --check --diff .

format:
	@echo "Formatting code..."
	black .
	isort .

.PHONY: help setup run-dev run-docker test test-endpoint test-func coverage clean lint format