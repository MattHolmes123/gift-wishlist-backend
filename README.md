# gift-wishlist-backend
Rest API backend for gift-wishlist application  

[![Tests Status](https://github.com/MattHolmes123/gift-wishlist-backend/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/MattHolmes123/gift-wishlist-backend/actions?query=workflow%3ABuild+branch%3Amain+event%3Apush)

## Project Dependencies
- Poetry: https://python-poetry.org/docs/#installation
- Docker: https://docs.docker.com/engine/install/

Once the above dependencies have been installed run the following:   
`./scripts/run-setup-local.sh`

This creates a virtual environment using poetry located in the project root `.venv` directory.  
This is to allow tools like pycharm to use the venv as the project interpreter.


## Local deployment:
- Run the database database: `docker-compose -f docker-compose.yml up`
- If this is the first time running the migrations should now be applied (See "Run migrations" below)
- Run the local uvicorn web server: `./scripts/run-dev-server.sh`

## Tools
See `scripts` folder for several scripts.

Some examples shown below:
- Run the tests (written using pytest): `./scripts/run-tests.sh`
- Run all linting tools: `./scripts/check-all.sh`
- Format python code: `./scripts/format-black.sh`

## Database Migration tool:
Database migrations are handled using alembic, ensure they are run before starting dev server.  
All files are localed in `./alembic`and `./alembic.ini`

Activate the .venv and then the following commands are available to you
- Run migrations: `PYTHONPATH=. alembic upgrade head` 
- Add a new migration `PYTHONPATH=. alembic revision --autogenerate -m "Add some table"`  

Check alembic docs for more info: https://alembic.sqlalchemy.org/en/latest/
