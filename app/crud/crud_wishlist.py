from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from app.models.user import User
from app.models.wishlist import WishListItem
from app.schemas.wishlist import WishListItemCreate, WishListItemUpdate

from .base import CRUDBase


class CrudWishListItem(CRUDBase[WishListItem, WishListItemCreate, WishListItemUpdate]):
    def __init__(self, *args, **kwargs):
        super(CrudWishListItem, self).__init__(*args, **kwargs)

    def get_user_wishlist(
        self, db: Session, u: User, *, skip: int = 0, limit: int = 100
    ) -> list[WishListItem]:
        query: Query = db.query(self.model).filter_by(user_id=u.id)

        return query.offset(skip).limit(limit).all()


wishlist_item = CrudWishListItem(WishListItem)
