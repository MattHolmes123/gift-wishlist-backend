#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-isort.sh

echo "Add --diff for detailed output"

poetry run isort app --check-only
