#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-isort.sh

echo "Add --diff for detailed output"

source $(poetry env info --path)/bin/activate

isort app --check-only

deactivate
