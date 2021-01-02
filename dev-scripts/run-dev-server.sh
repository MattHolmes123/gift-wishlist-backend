#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

. ./.venv/bin/activate
# Check alembic migrations
PYTHONPATH=.  python3 ./database/check-migrations.py

# TODO: Work out how to setup paths correctly with poetry
# poetry run ./database/check-migrations.py
deactivate

echo "starting uvicorn"
poetry run uvicorn app.main:app --reload --port 8081 \
  --reload-dir ./app \
  --reload-dir ./database \
  --reload-dir ./routers \
  --reload-dir ./wishlist
