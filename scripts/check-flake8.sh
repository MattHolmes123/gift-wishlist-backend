#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-flake8.sh

poetry run flake8 --count ./app
