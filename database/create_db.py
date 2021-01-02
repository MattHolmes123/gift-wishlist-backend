from alembic import command
from alembic.config import Config

from database.db import Base, engine


# this isn't used currently.
def create_local_database():
    # inside of a "create the database" script, first create
    # tables:
    Base.metadata.create_all(engine)
    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")


if __name__ == "__main__":
    create_local_database()
