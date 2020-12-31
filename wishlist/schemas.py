from typing import Optional

from pydantic import BaseModel, HttpUrl


class WishListItemBase(BaseModel):
    name: str
    url: HttpUrl


class WishListItemCreate(WishListItemBase):
    pass


# Not inherited from WishListItemBase to get around MyPy warnings.
class WishListItemUpdate(BaseModel):
    name: Optional[str]
    url: Optional[HttpUrl]


class WishListItem(WishListItemBase):
    id: int

    class Config:
        orm_mode = True
