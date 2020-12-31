from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import playground

import wishlist.routes

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
]

# Read this for more information:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
# https://fastapi.tiangolo.com/tutorial/cors/?h=+access+control+allow+origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This isn't a real router, its just to get used to fast api
app.include_router(playground.router)

app.include_router(wishlist.routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
