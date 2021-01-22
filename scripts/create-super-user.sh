#!/bin/bash

. ./.venv/bin/activate
# Check alembic migrations
PYTHONPATH=.  python3 app/database/create_super_user.py
