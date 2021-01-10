#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-pylint.sh

poetry run pylint -j 4 \
    app/database \
    app/routers \
    app/tests  \
    app/wishlist
