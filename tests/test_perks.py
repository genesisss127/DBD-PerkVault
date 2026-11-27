
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from database import Base, get_db
from main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    main.app.dependency_overrides[get_db] = override_get_db    
    Base.metadata.drop_all(bind=test_engine)


sample_perk = {
    "name": "Test Perk",
    "character": "Dwight Fairfield",
    "description": "A test perk description.",
    "icon": "/static/icons/test.png"
}


def test_create_perk(client):
    response = client.post("/perks/", json=sample_perk)

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_perk["name"]
    assert data["character"] == sample_perk["character"]
    assert data["description"] == sample_perk["description"]
    assert data["icon"] == sample_perk["icon"]


def test_get_all_perks(client):
    client.post("/perks/", json=sample_perk)

    response = client.get("/perks/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_perk["name"]


def test_get_single_perk(client):
    create_response = client.post("/perks/", json=sample_perk)
    perk_id = create_response.json()["id"]

    response = client.get(f"/perks/{perk_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == perk_id
    assert data["name"] == sample_perk["name"]
    assert data["character"] == sample_perk["character"]


def test_update_perk(client):
    create_response = client.post("/perks/", json=sample_perk)
    perk_id = create_response.json()["id"]

    updated_perk = {
        "name": "Updated Test Perk",
        "character": "Meg Thomas",
        "description": "Updated description.",
        "icon": "/static/icons/updated.png"
    }

    response = client.put(
        f"/perks/{perk_id}",
        json=updated_perk
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == updated_perk["name"]
    assert data["character"] == updated_perk["character"]
    assert data["description"] == updated_perk["description"]
    assert data["icon"] == updated_perk["icon"]


def test_delete_perk(client):
    create_response = client.post("/perks/", json=sample_perk)
    perk_id = create_response.json()["id"]

    response = client.delete(f"/perks/{perk_id}")

    assert response.status_code == 204

    check_response = client.get(f"/perks/{perk_id}")
    assert check_response.status_code == 404
