#!/bin/bash

# Should be run from root of project.
# e.g.
# ./scripts/create-environment-variables.sh

# TODO: Create a python script to get input from user
# for now just copy the env file
echo "Creating .env file in project root folder"
cp ./setup/samples/sample-local.env .env
