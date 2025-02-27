#!/bin/bash
# Script to run the test suite in Docker

set -e

# Ensure we're in the project root directory
cd "$(dirname "$0")/.."

# Build the tests container
echo "Building test containers..."
docker-compose -f tests/docker-compose.test.yml build

# Parse command-line arguments
TEST_TYPE=""
TEST_PATH=""
ADDITIONAL_ARGS=""

if [ "$1" = "endpoint" ]; then
    TEST_TYPE="endpoint"
    TEST_PATH="tests/endpoint/"
    shift
elif [ "$1" = "functionality" ]; then
    TEST_TYPE="functionality"
    TEST_PATH="tests/functionality/"
    shift
fi

# Any remaining arguments will be passed to pytest
if [ $# -gt 0 ]; then
    ADDITIONAL_ARGS="$@"
fi

# Determine the final pytest arguments
if [ -z "$TEST_PATH" ]; then
    PYTEST_ARGS="tests/"
else
    PYTEST_ARGS="$TEST_PATH"
fi

if [ -n "$ADDITIONAL_ARGS" ]; then
    PYTEST_ARGS="$PYTEST_ARGS $ADDITIONAL_ARGS"
fi

echo "Running tests with: $PYTEST_ARGS"

# Run the tests
docker-compose -f tests/docker-compose.test.yml run --rm \
    -e PYTEST_ARGS="$PYTEST_ARGS" \
    api_test

# Check exit code
if [ $? -eq 0 ]; then
    echo "Tests completed successfully!"
else
    echo "Tests failed!"
    exit 1
fi

# Clean up
echo "Cleaning up..."
docker-compose -f tests/docker-compose.test.yml down