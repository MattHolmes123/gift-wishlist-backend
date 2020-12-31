#!/bin/bash

echo ">>>> Exporting poetry requirements to requirements.txt"
poetry export -f requirements.txt --dev --without-hashes --output requirements.txt

echo ">>>> Creating project venv"
rm -rf venv
virtualenv -p python3.8 venv

echo ">>>> Activating venv"
. venv/bin/activate

echo ">>>> Upgrading pip"
./venv/bin/python -m pip install --upgrade pip

echo ">>>> Installing project dependencies"
pip install -r requirements.txt
