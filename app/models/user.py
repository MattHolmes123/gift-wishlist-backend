from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# TODO create a baseclass file
# from app.db.base_class import Base
from app.database.db import Base


class User(Base):
    """User model"""

    __tablename__ = "user"

    # keys
    id = Column(Integer, primary_key=True, index=True)

    # relationships
    items = relationship(
        "app.models.wishlist.WishListItem", back_populates="user", cascade="all, delete"
    )

    # columns
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
