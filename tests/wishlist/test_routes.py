from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import status

from database.db import Base
from app.main import app
from wishlist.routes import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_get_and_update_wishlist_item():

    # Test CREATE
    response = client.post(
        "/wishlist/items/",
        json={"name": "Boots", "url": "https://i-want-some-boots.com"},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Boots"

    assert "id" in data
    item_id = data["id"]

    # Test GET
    response = client.get(f"/wishlist/items/{item_id}")

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Boots"
    assert data["id"] == item_id

    # Test UPDATE
    response = client.put(f"/wishlist/items/{item_id}", json={"name": "Big Boots"})

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Big Boots"
    assert data["id"] == item_id


def test_unknown_item_returns_correct_status():
    response = client.get("/wishlist/items/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"

    response = client.put("/wishlist/items/999", json={"name": "Unknown boots"})
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"


def test_put_validation():
    response = client.put("/wishlist/items/999")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
