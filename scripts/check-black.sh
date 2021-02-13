#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-black.sh

source $(poetry env info --path)/bin/activate

black --check ./app

deactivate
