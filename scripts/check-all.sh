#!/bin/bash

BLUE='\033[1;34m'
NO_COLOR='\033[0m'

# Uncomment if we want black to fail if it finds things it would change.
# set -e

printf "%bRunning Black checks%b\n" "$BLUE" "$NO_COLOR"
./scripts/check-black.sh

printf "%bRunning isort checks%b\n" "$BLUE" "$NO_COLOR"
./scripts/check-isort.sh

printf "%bRunning flake8 checks%b\n" "$BLUE" "$NO_COLOR"
./scripts/check-flake8.sh

printf "%bRunning pylint checks%b\n" "$BLUE" "$NO_COLOR"
./scripts/check-pylint.sh

printf "%bRunning mypy checks%b\n" "$BLUE" "$NO_COLOR"
./scripts/check-mypy.sh

printf "%bAll tests finished%b\n" "$BLUE" "$NO_COLOR"
