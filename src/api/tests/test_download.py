from fastapi.testclient import TestClient
from api.main import app
import os

client = TestClient(app)

def test_download_file():
    # Prima genera un file CSV
    payload = {
        "data": [{"Nome": "Alice", "Età": 30}, {"Nome": "Bob", "Età": 25}]
    }
    response = client.post("/export/csv", json=payload)
    assert response.status_code == 200
    result = response.json()
    filename = result["filename"]
    # Ora scarica il file
    download_response = client.get(f"/downloads/{filename}")
    assert download_response.status_code == 200
    assert download_response.content
    # Verifica che il contenuto sia quello atteso (header CSV)
    assert b"Nome" in download_response.content 