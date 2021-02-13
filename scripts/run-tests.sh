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

# TODO: Remove disable warnings flag
poetry run pytest --disable-warnings "$@"
