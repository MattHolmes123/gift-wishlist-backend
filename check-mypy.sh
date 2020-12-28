#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# before poetry
# source venv/bin/activate
# mypy --ignore-missing-imports --allow-untyped-globals "$@" .

poetry run mypy --ignore-missing-imports --allow-untyped-globals "$@" .
