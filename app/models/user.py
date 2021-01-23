from sqlalchemy import Boolean, Column, Integer, String

# TODO create a baseclass file
# from app.db.base_class import Base
from app.database.db import Base


# Add back in when refactoring Wishlish app
# from sqlalchemy.orm import relationship

# if TYPE_CHECKING:
#     from app.wishlist.models import WishListItem  # noqa: F401


class User(Base):
    """User model"""

    __tablename__ = "user"

    # keys
    id = Column(Integer, primary_key=True, index=True)

    # relationships
    # items = relationship("WishlistItem", back_populates="user")

    # columns
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
