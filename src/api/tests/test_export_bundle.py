from fastapi.testclient import TestClient
from api.main import app
import os

client = TestClient(app)

def test_export_bundle():
    payload = {
        "data": [{"Nome": "Alice", "Età": 30}, {"Nome": "Bob", "Età": 25}]
    }
    response = client.post("/export/bundle", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "filename" in result
    assert result["filename"].endswith(".zip")
    filepath = os.path.join("src/api/downloads", result["filename"])
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0 