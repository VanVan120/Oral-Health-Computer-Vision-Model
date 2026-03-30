from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    # Test valid registration
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "role": "patient"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test duplicate registration
    response2 = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User 2",
            "role": "patient"
        }
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"

def test_login_user(client: TestClient):
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpassword123",
            "name": "Login User",
            "role": "patient"
        }
    )

    # Test valid login
    response = client.post(
        "/auth/token",
        data={
            "username": "login@example.com",
            "password": "loginpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Test invalid login (wrong password)
    response_invalid = client.post(
        "/auth/token",
        data={
            "username": "login@example.com",
            "password": "wrongpassword"
        }
    )
    assert response_invalid.status_code == 401

def test_get_doctors(client: TestClient):
    # Register a doctor
    client.post(
        "/auth/register",
        json={
            "email": "doc@example.com",
            "password": "docpassword123",
            "name": "Dr. Test",
            "role": "doctor"
        }
    )
    
    response = client.get("/auth/doctors")
    assert response.status_code == 200
    doctors = response.json()
    assert isinstance(doctors, list)
    assert len(doctors) >= 1
    assert any(d["name"] == "Dr. Test" for d in doctors)
