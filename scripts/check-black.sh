#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/check-black.sh

poetry run black --check ./app
