from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.database.db import get_db

router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"],
    dependencies=[Depends(deps.get_current_active_user)],
)


@router.get("/items/", response_model=schemas.WishListList)
def get_all_wishlist_items(
    db: Session = Depends(get_db),
    superuser: models.User = Depends(deps.get_current_active_superuser),
    list_qs: deps.ListQueryParams = Depends(),
):

    items = crud.wishlist_item.get_multi(
        db,
        skip=list_qs.skip,
        limit=list_qs.limit,
    )

    return items


# get user id items
# get self wishlist items


@router.post("/items/", response_model=schemas.WishListItem)
def create_wishlist_item(
    item: schemas.WishListItemCreate, db: Session = Depends(get_db)
):

    return crud.wishlist_item.create(db, obj_in=item)


@router.get(
    "/items/{item_id}",
    response_model=schemas.WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def get_wishlist_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.wishlist_item.get(db, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    return item


@router.put(
    "/items/{item_id}",
    response_model=schemas.WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def update_wishlist_item(
    item_id: int, item: schemas.WishListItemUpdate, db: Session = Depends(get_db)
):

    db_obj = crud.wishlist_item.get(db, item_id)

    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    db_obj = crud.wishlist_item.update(db, db_obj=db_obj, obj_in=item)

    return db_obj
