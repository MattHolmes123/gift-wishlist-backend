#!/bin/bash

source $(poetry env info --path)/bin/activate
# Check alembic migrations
PYTHONPATH=.  python3 app/database/create_superuser.py
