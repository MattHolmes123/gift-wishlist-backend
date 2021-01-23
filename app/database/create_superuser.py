from app import crud, schemas
from app.core.config import settings
from app.database.db import SessionLocal, Session


def create_initial_superuser(db: Session) -> None:
    """Create a super user account.

    :param db: Database connection
    :return: None
    """

    env_variables_needed = ["FIRST_SUPERUSER", "FIRST_SUPERUSER_PASSWORD"]
    e_vars = ", ".join(env_variables_needed)
    assert (
        settings.first_superuser
    ), f"Can't create superuser without the following environment variables: {e_vars}"

    user = crud.user.get_by_email(db, email=settings.first_superuser)

    if not user:
        user_in = schemas.user.UserCreate(
            email=settings.first_superuser,
            password=settings.first_superuser_password,
            is_superuser=True,
            full_name="First Superuser",
        )

        user = crud.user.create(db, obj_in=user_in)

    print(f"Super user: {user}")


if __name__ == "__main__":
    session = SessionLocal()
    create_initial_superuser(session)
