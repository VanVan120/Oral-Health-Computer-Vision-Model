import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
import os
import sys

# Add the project root to the python path so tests can run easily
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from core.database import get_session
import core.models

# Setup an in-memory test database
test_sqlite_url = "sqlite://"
test_engine = create_engine(test_sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)

def get_session_override():
    with Session(test_engine) as session:
        yield session

# Override the application's dependencies for testing
app.dependency_overrides[get_session] = get_session_override

@pytest.fixture(name="session")
def session_fixture():
    # Create tables
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    # Drop tables after test
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    with TestClient(app) as client:
        yield client
    
@pytest.fixture(name="patient_token")
def patient_token_fixture(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "patient@example.com",
            "password": "password123",
            "name": "Patient Test",
            "role": "patient"
        }
    )
    res = client.post(
        "/auth/token",
        data={"username": "patient@example.com", "password": "password123"}
    )
    return res.json()["access_token"]

@pytest.fixture(name="doctor_token")
def doctor_token_fixture(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "doctor@example.com",
            "password": "password123",
            "name": "Doctor Test",
            "role": "doctor"
        }
    )
    res = client.post(
        "/auth/token",
        data={"username": "doctor@example.com", "password": "password123"}
    )
    return res.json()["access_token"]
