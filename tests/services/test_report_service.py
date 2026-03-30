import pytest
from services.report_service import generate_expert_report, generate_public_report

@pytest.fixture
def mock_analysis_data():
    return {
        "model_used": "Model A (Histopathology)",
        "prediction": {"class": "OSCC", "confidence": 0.95},
        "details": {
            "cell_analysis": {
                "cancerous_cells": 120,
                "stroma_cells": 40,
                "necrosis_cells": 10
            }
        }
    }

def test_generate_expert_report(mock_analysis_data):
    # Test expert report generation without an image
    pdf_bytes = generate_expert_report(mock_analysis_data)
    
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF files start with %PDF
    assert pdf_bytes.startswith(b"%PDF-")

def test_generate_public_report(mock_analysis_data):
    # Test public report generation without an image
    pdf_bytes = generate_public_report(mock_analysis_data)
    
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF files start with %PDF
    assert pdf_bytes.startswith(b"%PDF-")
