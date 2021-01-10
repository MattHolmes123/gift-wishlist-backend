# Everything in here is just an example to play around with fast-api
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/playground", tags=["playground"])


# This is just a mess around
class PlaygroundListItem(BaseModel):
    msg: str
    foo: int
    bar: int
    baz: int


class AppState(BaseModel):
    count: int
    playground_list_data: List[PlaygroundListItem]


@router.get("/get-app-state", response_model=AppState)
async def get_app_state():
    return {
        "count": 42,
        "playground_list_data": [
            {"msg": "First message", "foo": 1, "bar": 2, "baz": 3},
            {"msg": "Second message", "foo": 11, "bar": 22, "baz": 33},
        ],
    }
