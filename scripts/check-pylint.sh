#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-pylint.sh

set -e

source $(poetry env info --path)/bin/activate

pylint -j 4 \
    app/database \
    app/routers \
    app/tests  \
    app/wishlist

deactivate
