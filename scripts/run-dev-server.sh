#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

poetry run check-migrations

source $(poetry env info --path)/bin/activate

echo "starting uvicorn"
uvicorn app.main:app --reload --port 8081 --reload-dir ./app

deactivate
