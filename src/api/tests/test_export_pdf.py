from fastapi.testclient import TestClient
from api.main import app
import os

client = TestClient(app)

def test_export_pdf():
    payload = {
        "data": {"Titolo": "Analisi", "Sentiment": "Positivo", "Tags": "AI, tool"}
    }
    response = client.post("/export/pdf", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "filename" in result
    assert result["filename"].endswith(".pdf")
    filepath = os.path.join("src/api/downloads", result["filename"])
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0 