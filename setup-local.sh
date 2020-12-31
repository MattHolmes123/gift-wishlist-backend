#!/bin/bash

echo "Installing project dependencies (including dev dependencies)"
# https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean
poetry config virtualenvs.in-project true --local
poetry install
