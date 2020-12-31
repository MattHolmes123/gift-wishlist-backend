from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_wishlist_item(
    db: Session, item: schemas.WishListItemCreate
) -> models.WishListItem:
    """Create a wishlist item.

    :param db: Database connection
    :param item: New item to create
    :return: Newly created item
    """

    wishlist_item = models.WishListItem(name=item.name, url=item.url)

    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)

    return wishlist_item


def get_wishlist_item(db: Session, item_id: int) -> Optional[models.WishListItem]:
    """Get a wishlist item.

    :param db: Database connection
    :param item_id: Primary key of item
    :return: Wishlist item or none
    """

    return (
        db.query(models.WishListItem).filter(models.WishListItem.id == item_id).first()
    )


def update_wishlist_item(
    db: Session, item_id: int, item: schemas.WishListItemUpdate
) -> Optional[models.WishListItem]:
    """Update a wishlist item.

    :param db: Database connection
    :param item_id: Primary key of item
    :param item: Item data
    :return: Wishlist item
    """

    record = get_wishlist_item(db, item_id)

    if record is None:
        return None

    updates = item.dict(exclude_unset=True)

    for field, value in updates.items():
        print(f"Setting key: {field}, with value: {value}")
        setattr(record, field, value)

    db.commit()

    db.refresh(record)

    return record
