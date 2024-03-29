"""Main file to setup app and include all routes."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.routers import playground

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
]

# Read these for more information:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
# https://fastapi.tiangolo.com/tutorial/cors/?h=+access+control+allow+origin
# https://javascript.info/fetch-crossorigin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This isn't a real router, its just to get used to fast api
app.include_router(playground.router)
app.include_router(api_router)


@app.get("/")
async def root():
    """Sample route, need to remove.

    :return: Sample data
    """

    return {"message": "Hello World"}
