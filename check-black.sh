#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# before poetry
# source venv/bin/activate
# black --check .

poetry run black --check .
