#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/run-tests.sh

echo "Removing test database"
rm app/tests/test.db

# to ensure the settings.environment setting is set to test
echo "Setting environment variables"
export SECRET_KEY="test-secret-key"
export ENVIRONMENT="test"

echo "running tests"
poetry run pytest
