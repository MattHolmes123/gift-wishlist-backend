#!/bin/bash

# to ensure the settings.environment setting is set to test

echo "Removing test database"
rm tests/test.db

# to ensure the settings.environment setting is set to test
echo "Setting environment variables"
export ENVIRONMENT="test"

echo "running tests with coverage"
poetry run coverage run -m pytest

poetry run coverage report
