from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_graphql():
    response = client.post(
        "/graphql",
        json={"query": "{ hello }"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["hello"].startswith("Hello,")
