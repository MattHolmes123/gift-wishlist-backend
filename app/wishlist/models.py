from sqlalchemy import Column, Integer, String  # , ForeignKey

from app.database.db import Base

# TODO: Add back in when refactoring wishlist app
# from sqlalchemy.orm import relationship


class WishListItem(Base):
    """Wishlist item model - Items the users wishes to have"""

    __tablename__ = "wishlist_item"

    # keys
    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("user.id"))

    # relationships
    # user = relationship("User", back_populates="items")

    # columns
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
