from sqlalchemy import Column, Integer, String

from app.database.db import Base


class WishListItem(Base):
    __tablename__ = "wishlist_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
