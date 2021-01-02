#!/bin/bash

# Should be run from root of project.
# e.g.
# ./dev-scripts/check-mypy.sh

poetry run mypy --ignore-missing-imports --allow-untyped-globals "$@" .
