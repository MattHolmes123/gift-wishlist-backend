#!/bin/bash

# Should be run from root of project.
# e.g.
# ./dev-scripts/format-black.sh

poetry run black .
