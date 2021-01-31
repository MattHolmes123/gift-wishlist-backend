from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.db import Base


class WishListItem(Base):
    """Wishlist item model - Items the users wishes to have"""

    __tablename__ = "wishlist_item"

    # keys
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # relationships
    user = relationship("app.models.user.User", back_populates="items")

    # columns
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
