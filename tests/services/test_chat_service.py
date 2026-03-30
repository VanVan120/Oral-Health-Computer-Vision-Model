import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Must mock the google generatveai to avoid API errors if key is not set
@patch("services.chat_service.genai.GenerativeModel")
def test_chat_feedback(mock_genai, client: TestClient, patient_token: str):
    headers = {"Authorization": f"Bearer {patient_token}"}
    
    # Payload matching FeedbackCreate
    payload = {
        "prompt": "What is this?",
        "gemini_response": "This is an example",
        "is_helpful": True,
        "user_correction": None
    }
    
    response = client.post("/api/chat/feedback", headers=headers, json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

@patch("services.chat_service.genai.GenerativeModel")
def test_chat_feedback_unauthorized(mock_genai, client: TestClient):
    payload = {
        "chat_history": '[]',
        "user_rating": 3,
        "comments": "Will fail"
    }
    
    response = client.post("/api/chat/feedback", json=payload)
    assert response.status_code == 401
