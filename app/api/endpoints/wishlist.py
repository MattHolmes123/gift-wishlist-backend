from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database.db import get_db
from app.schemas import WishListItem, WishListItemCreate, WishListItemUpdate

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get(
    "/items/{item_id}",
    response_model=WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def get_wishlist_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.wishlist_item.get(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    return item


@router.post("/items/", response_model=WishListItem)
def create_wishlist_item(item: WishListItemCreate, db: Session = Depends(get_db)):

    return crud.wishlist_item.create(db, obj_in=item)


@router.put(
    "/items/{item_id}",
    response_model=WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def update_wishlist_item(
    item_id: int, item: WishListItemUpdate, db: Session = Depends(get_db)
):

    db_obj = crud.wishlist_item.get(db, item_id)

    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    db_obj = crud.wishlist_item.update(db, db_obj=db_obj, obj_in=item)

    return db_obj
