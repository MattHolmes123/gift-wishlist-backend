#! /bin/bash

. venv/bin/activate

uvicorn main:app --reload --port 8080
