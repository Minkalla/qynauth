from fastapi.testclient import TestClient
from app.main import app, users_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "QynAuth MVP"}


def test_register_user_success():
    user_db.clear()

    response = client.post(
        "/auth/register",
        json={"username": "testuser1", "password": "securepassword123"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"
    assert "user_id" in response.json()
    assert response.json()["username"] == "testuser1"
    assert "testuser1" in user_db


def test_register_user_conflict():
    user_db.clear()
    client.post(
        "/auth/register",
        json={"username": "existinguser", "password": "password"},
    )

    response = client.post(
        "/auth/register",
        json={"username": "existinguser", "password": "anotherpassword"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already registered"


def test_login_success():
    user_db.clear()
    client.post(
        "/auth/register",
        json={"username": "loginuser", "password": "loginpassword"},
    )

    response = client.post(
        "/auth/login",
        json={"username": "loginuser", "password": "loginpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["user_id"] is not None


def test_login_incorrect_password():
    user_db.clear()
    client.post(
        "/auth/register",
        json={"username": "wrongpassuser", "password": "correctpassword"},
    )

    response = client.post(
        "/auth/login",
        json={"username": "wrongpassuser", "password": "incorrectpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_nonexistent_user():
    user_db.clear()
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "anypassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
