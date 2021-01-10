#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/format-black.sh

poetry run black ./app
