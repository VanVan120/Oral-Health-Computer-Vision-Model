import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from services import chat_service

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


def test_sanitize_analysis_context_omits_binary_fields():
    raw_context = {
        "predictions": {
            "abnormality_detected": True,
            "confidence": 0.99,
            "heatmap_overlay": "A" * 512,
            "original_resized": "B" * 1024,
            "notes": "short note"
        }
    }

    sanitized = chat_service._sanitize_analysis_context(raw_context)

    assert sanitized["predictions"]["abnormality_detected"] is True
    assert sanitized["predictions"]["confidence"] == 0.99
    assert sanitized["predictions"]["heatmap_overlay"] == "[omitted_binary_data]"
    assert sanitized["predictions"]["original_resized"] == "[omitted_binary_data]"
    assert sanitized["predictions"]["notes"] == "short note"


def test_clean_suggestion_response_filters_reasoning_text():
    noisy_output = """
    Helpful, empathetic, professional medical assistant for an Oral Cancer AI Platform.
    1. No Diagnosis: Do not say direct diagnosis.
    * Draft 1: The model detected abnormal cells and suggests review.
    The analysis suggests a high likelihood of abnormality (99.9% confidence), specifically detecting nuclear hyperchromatism and multiple nucleoli across 25 abnormal cells.
    A comprehensive review by a board-certified pathologist is recommended for definitive confirmation.
    The analysis suggests a high likelihood of abnormality (99.9% confidence), specifically detecting nuclear hyperchromatism and multiple nucleoli across 25 abnormal cells.
    A comprehensive review by a board-certified pathologist is recommended for definitive confirmation.
    """

    cleaned = chat_service._clean_suggestion_response(noisy_output, max_sentences=2)

    assert "Helpful, empathetic" not in cleaned
    assert "Draft 1" not in cleaned
    assert "No Diagnosis" not in cleaned
    assert cleaned.count("The analysis suggests") == 1
    assert cleaned.count("board-certified pathologist") == 1


def test_clean_chat_response_removes_meta_reasoning_sections():
    noisy_chat = """
    User Question: "what is oral cancer"
    Analysis Context: {} (Empty/Not provided)
    Role: Helpful, empathetic, professional medical assistant for an Oral Cancer AI Platform.
    Constraints: No diagnosis, always advise consultation, context-aware, calm/supportive tone.
    Guideline 1 (No Diagnosis): Not applicable here.
    Introduction: Define oral cancer clearly.

    Oral cancer refers to malignant (cancerous) growths that develop in any part of the oral cavity.
    Early detection is key to successful treatment. If you have concerns, please schedule an appointment with a specialist.
    """

    cleaned = chat_service._clean_chat_response(noisy_chat)

    assert "User Question:" not in cleaned
    assert "Analysis Context:" not in cleaned
    assert "Role:" not in cleaned
    assert "Constraints:" not in cleaned
    assert "Guideline 1" not in cleaned
    assert "Introduction:" not in cleaned
    assert "Oral cancer refers to malignant" in cleaned
    assert "please schedule an appointment with a specialist" in cleaned.lower()


def test_clean_chat_response_keeps_final_answer_when_scaffold_leaks():
    noisy_chat = """
    Role: Helpful, empathetic, professional medical assistant for an Oral Cancer AI Platform.
    The AI likely uses computer vision/machine learning to analyze images of the oral cavity.
    It compares user-uploaded images against a large dataset of known healthy and pathological oral tissues.
    It identifies patterns, colors, and textures associated with various conditions.
    Professional and Calm: "Our AI platform uses advanced machine learning and computer vision technology..."
    Empathetic/Supportive: "It is designed to act as a screening tool to help you and your healthcare provider identify potential issues early."
    No Diagnosis: Ensure it's framed as suggesting patterns, not diagnosing.
    Consultation: Must end with a recommendation to see a specialist.
    Explain the process: Image upload -> Analysis against dataset -> Pattern recognition -> Result generation.
    Clarify that it's a tool, not a replacement for a doctor.

    Our AI platform utilizes advanced machine learning and computer vision technology to analyze images of the oral cavity. The model has been trained on a vast dataset of clinical images, allowing it to recognize specific patterns, textures, and color variations associated with various oral conditions. When you upload an image, the AI scans the area for anomalies and compares them against these learned patterns to detect potential issues. It is important to remember that the AI is designed as a screening tool to highlight areas of concern; it does not provide a definitive medical diagnosis. Because an accurate diagnosis requires a physical examination and potentially a biopsy, we strongly recommend that you consult with a licensed dentist or oral pathologist to review your results and receive a professional evaluation.
    AI ASSISTANT • JUST NOW
    """

    cleaned = chat_service._clean_chat_response(noisy_chat)

    assert "Role:" not in cleaned
    assert "Professional and Calm" not in cleaned
    assert "No Diagnosis:" not in cleaned
    assert "Explain the process:" not in cleaned
    assert "The AI likely uses" not in cleaned
    assert "AI ASSISTANT" not in cleaned
    assert cleaned.startswith("Our AI platform utilizes advanced machine learning and computer vision technology")
    assert "licensed dentist or oral pathologist" in cleaned
