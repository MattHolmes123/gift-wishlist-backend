#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-mypy.sh

set -e

source $(poetry env info --path)/bin/activate

mypy --config-file mypy.ini "$@" app

deactivate
