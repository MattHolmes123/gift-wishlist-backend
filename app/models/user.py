from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# TODO create a baseclass file
# from app.db.base_class import Base
from app.database.db import Base

if TYPE_CHECKING:
    from app.models import WishListItem


class User(Base):
    """User model"""

    __tablename__ = "user"

    # keys
    id: int = Column(Integer, primary_key=True, index=True)

    # relationships
    items: list["WishListItem"] = relationship(
        "app.models.wishlist.WishListItem", back_populates="user", cascade="all, delete"
    )

    # columns
    full_name = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)

    def __str__(self):
        return (
            f"User("
            f"id={self.id!r}, "
            f"full_name={self.full_name!r}, "
            f"email={self.email!r}, "
            f"is_active={self.is_active!r}, "
            f"is_superuser={self.is_superuser!r}"
            f")"
        )
