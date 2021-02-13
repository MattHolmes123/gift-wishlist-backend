import sqlalchemy

from alembic import config, script
from alembic.runtime import migration
from app.core.config import settings


def main():
    """Script entry point

    :return: None
    """

    check()


def check():
    """Check if all the migrations have been ran

    :return: None
    """

    engine = sqlalchemy.create_engine(settings.pg_dsn)

    alembic_cfg = config.Config("alembic.ini")
    script_ = script.ScriptDirectory.from_config(alembic_cfg)

    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)

        if context.get_current_revision() != script_.get_current_head():
            raise Exception("Upgrade the database.")

        else:
            print("Latest Migrations applied")


if __name__ == "__main__":
    main()
