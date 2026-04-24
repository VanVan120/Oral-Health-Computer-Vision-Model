from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_read_about(client: TestClient):
    response = client.get("/about")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

from unittest.mock import patch, MagicMock
import io

def test_chat_endpoint(client: TestClient):
    with patch("main.get_chat_response", return_value="Mocked AI Response") as mock_chat:
        response = client.post(
            "/chat",
            json={
                "message": "What is OSCC?",
                "context": {"model_used": "Model A"}
            }
        )
        assert response.status_code == 200
        assert response.json() == {"reply": "Mocked AI Response"}
        mock_chat.assert_called_once_with("What is OSCC?", {"model_used": "Model A"})


def test_get_suggestion_uses_suggestion_mode(client: TestClient):
    payload = {
        "model_type": "Model A",
        "analysis_data": {
            "predictions": {
                "abnormality_detected": True,
                "confidence": 0.99,
                "heatmap_overlay": "AAA"
            }
        }
    }

    with patch("main.get_chat_response", return_value="Clean suggestion.") as mock_chat:
        response = client.post("/api/get-suggestion", json=payload)

    assert response.status_code == 200
    assert response.json() == {"ai_suggestion": "Clean suggestion."}
    assert mock_chat.call_count == 1

    args, kwargs = mock_chat.call_args
    assert "histopathology" in args[0].lower()
    assert args[1] == payload["analysis_data"]
    assert kwargs["mode"] == "suggestion"

@patch("main.TriageRouter")
@patch("main.ModelAInference")
@patch("main.OralHygieneModel")
def test_analyze_endpoint_model_a(mock_model_b, mock_model_a, mock_triage, client: TestClient):
    # Mock the triage to route to Model A
    mock_triage_instance = mock_triage.return_value
    mock_triage_instance.predict.return_value = "Histopathological"
    
    # Mock Model A prediction
    mock_model_a_instance = mock_model_a.return_value
    mock_model_a_instance.predict.return_value = {
        "class": "OSCC",
        "confidence": 0.99
    }
    
    # We must mock the actual instantiated objects in main.py namespace!
    with patch("main.triage_router", mock_triage_instance), \
         patch("main.model_a", mock_model_a_instance), \
         patch("main.model_b", None), \
         patch("main.get_chat_response", return_value="See a doctor ASAP."):
         
        # Create a dummy image file
        dummy_img = io.BytesIO(b"dummy image data")
        
        response = client.post(
            "/analyze",
            files={"file": ("test_image.jpg", dummy_img, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["model_used"] == "Model A (Histopathology)"
        assert data["final_analysis"]["class"] == "OSCC"
        assert "triage_result" in data

