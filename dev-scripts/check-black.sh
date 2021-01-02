#!/bin/bash

# Should be run from root of project.
# e.g.
# ./dev-scripts/check-black.sh

poetry run black --check .
