#!/bin/bash

# Should be run from root of project.
# e.g.
# ./dev-scripts/check-pylint.sh

poetry run pylint -j 4 \
    database \
    routers \
    tests  \
    wishlist
