#!/bin/bash

# Should be run from root of project.
# e.g.
# ./dev-scripts/check-flake8.sh

poetry run flake8 .
