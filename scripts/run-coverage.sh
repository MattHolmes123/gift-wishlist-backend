#!/bin/bash

# to ensure the settings.environment setting is set to test

source $(poetry env info --path)/bin/activate

echo "Removing test database"
rm app/tests/test.db

# to ensure the settings.environment setting is set to test
echo "Setting environment variables"
export ENVIRONMENT="test"

echo "running tests with coverage"
coverage run -m pytest

coverage report

deactivate