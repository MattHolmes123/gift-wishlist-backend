#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

source $(poetry env info --path)/bin/activate

# Check alembic migrations
PYTHONPATH=.  python3 ./app/database/check-migrations.py

# TODO: Work out how to setup paths correctly with poetry (and run it as a script e.g. poetry run check-migrations)
# poetry run ./database/check-migrations.py
deactivate

echo "starting uvicorn"
poetry run uvicorn app.main:app --reload --port 8081 --reload-dir ./app
