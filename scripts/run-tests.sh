#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/run-tests.sh

echo "Removing test database"
rm tests/test.db

# to ensure the settings.environment setting is set to test
echo "Setting environment variables"
export ENVIRONMENT="test"

echo "running tests"
poetry run pytest
