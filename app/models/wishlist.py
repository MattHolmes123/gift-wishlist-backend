from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base

if TYPE_CHECKING:
    from app.models import User


class WishListItem(Base):
    """Wishlist item model - Items the users wishes to have"""

    __tablename__ = "wishlist_item"

    # keys
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # relationships
    user: "User" = relationship("app.models.user.User", back_populates="items")

    # columns
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    def __str__(self):
        return (
            f"WishListItem("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"name={self.name!r}, "
            f"url={self.url!r}"
            f")"
        )
