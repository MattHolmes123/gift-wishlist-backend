#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/format-black.sh

source $(poetry env info --path)/bin/activate

black ./app

deactivate
