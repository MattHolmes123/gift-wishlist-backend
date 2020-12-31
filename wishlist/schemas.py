from typing import Optional

from pydantic import BaseModel, HttpUrl


class WishListItemBase(BaseModel):
    name: str
    url: HttpUrl


class WishListItemCreate(WishListItemBase):
    pass


class WishListItemUpdate(WishListItemBase):
    name: Optional[str]
    url: Optional[HttpUrl]


class WishListItem(WishListItemBase):
    id: int

    class Config:
        orm_mode = True
