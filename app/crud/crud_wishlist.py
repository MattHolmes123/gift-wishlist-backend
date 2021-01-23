from app.models.wishlist import WishListItem
from app.schemas.wishlist import WishListItemCreate, WishListItemUpdate
from .base import CRUDBase


class CrudWishListItem(CRUDBase[WishListItem, WishListItemCreate, WishListItemUpdate]):
    def __init__(self, *args, **kwargs):
        super(CrudWishListItem, self).__init__(*args, **kwargs)


wishlist_item = CrudWishListItem(WishListItem)
