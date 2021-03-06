#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-mypy.sh

set -e

source $(poetry env info --path)/bin/activate

mypy --ignore-missing-imports --allow-untyped-globals "$@" ./app

deactivate
