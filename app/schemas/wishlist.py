from typing import Optional

from pydantic import BaseModel, HttpUrl


# Shared properties
class WishListItemBase(BaseModel):
    name: Optional[str]
    url: Optional[HttpUrl]


# Properties to receive via API on creation
class WishListItemCreate(WishListItemBase):
    name: str
    url: HttpUrl
    user_id: int


# Properties to receive via API on update
class WishListItemUpdate(WishListItemBase):
    pass


class WishListItemInDBBase(WishListItemBase):
    id: Optional[int] = None
    user_id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class WishListItem(WishListItemInDBBase):
    pass


# Additional properties stored in DB
class WishListItemInDB(WishListItemInDBBase):
    id: int
