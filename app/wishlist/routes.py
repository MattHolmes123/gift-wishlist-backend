from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import schemas, crud

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get(
    "/items/{item_id}",
    response_model=schemas.WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def get_wishlist_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_wishlist_item(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    return item


@router.post("/items/", response_model=schemas.WishListItem)
def create_wishlist_item(
    item: schemas.WishListItemCreate, db: Session = Depends(get_db)
):
    return crud.create_wishlist_item(db, item)


@router.put(
    "/items/{item_id}",
    response_model=schemas.WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def update_wishlist_item(
    item_id: int, item: schemas.WishListItemUpdate, db: Session = Depends(get_db)
):
    db_item = crud.update_wishlist_item(db, item_id, item)

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    return db_item
