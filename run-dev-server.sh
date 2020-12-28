#! /bin/bash

# echo "Activating venv"
#. venv/bin/activate

# echo "starting uvicorn"
# uvicorn main:app --reload --port 8080

poetry run uvicorn main:app --reload --port 8081
