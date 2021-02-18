#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-flake8.sh

set -e

source $(poetry env info --path)/bin/activate

flake8 --count ./app

deactivate
