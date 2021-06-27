from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.database.db import get_db

# Wishlist admin router and routes
admin_router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist-admin"],
    dependencies=[Depends(deps.get_current_active_superuser)],
)


@admin_router.get("/items", response_model=schemas.WishListList)
def get_all_wishlist_items(
    db: Session = Depends(get_db),
    list_qs: deps.ListQueryParams = Depends(),
) -> Any:
    """Fetch all wishlist items."""

    items = crud.wishlist_item.get_multi(db, skip=list_qs.skip, limit=list_qs.limit)

    return items


@admin_router.get("/items/user/{user_id}", response_model=schemas.WishListList)
def get_all_user_wishlist_items(
    user_id: int,
    db: Session = Depends(get_db),
    list_qs: deps.ListQueryParams = Depends(),
):
    """Get all wishlist items for the supplied user."""

    user = crud.user.get(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    items = crud.wishlist_item.get_user_wishlist(
        db, user, skip=list_qs.skip, limit=list_qs.limit
    )

    return items


# Wishlist router and routes
router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"],
    dependencies=[Depends(deps.get_current_active_user)],
)


@router.get("/items/me", response_model=schemas.WishListList)
def get_my_wishlist(
    db: Session = Depends(get_db),
    user: models.User = Depends(deps.get_current_active_user),
    list_qs: deps.ListQueryParams = Depends(),
) -> Any:
    """Get all wishlist items for the logged in user."""

    items = crud.wishlist_item.get_user_wishlist(
        db, user, skip=list_qs.skip, limit=list_qs.limit
    )

    return items


@router.post("/items", response_model=schemas.WishListItem)
def create_wishlist_item(
    item: schemas.WishListItemCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a wishlist item."""

    # TODO: Write tests for
    if user.id != item.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't add a wishlist item to another user's wishlist",
        )

    return crud.wishlist_item.create(db, obj_in=item)


@router.get(
    "/items/{item_id}",
    response_model=schemas.WishListItem,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Wish list item not found"}},
)
def get_wishlist_item(item_id: int, db: Session = Depends(get_db)) -> Any:
    """Get a wishlist item by ID."""

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
) -> Any:
    """Update a wishlist item by ID."""

    db_obj = crud.wishlist_item.get(db, item_id)

    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wish list item not found"
        )

    db_obj = crud.wishlist_item.update(db, db_obj=db_obj, obj_in=item)

    return db_obj
