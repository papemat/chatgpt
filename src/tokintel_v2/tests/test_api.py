import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from api.server import app

client = TestClient(app)

def test_root():
    """Test endpoint root"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "TokIntel v2.1 API"
    assert data["status"] == "running"

def test_health():
    """Test endpoint health"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.1.0"

def test_analyze_text():
    """Test analisi testo"""
    payload = {
        "content": "Questo è un video motivazionale per imprenditori #business #successo",
        "title": "Test Video"
    }
    response = client.post("/analyze/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "message" in data

def test_analyze_text_invalid():
    """Test analisi testo con payload invalido"""
    payload = {"invalid": "data"}
    response = client.post("/analyze/text", json=payload)
    assert response.status_code == 422  # Validation error

def test_analytics_endpoints():
    """Test endpoint analytics"""
    # Test top videos
    response = client.get("/analytics/top-videos")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    
    # Test sentiment trend
    response = client.get("/analytics/sentiment-trend")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    
    # Test keywords
    response = client.get("/analytics/keywords")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data

def test_analyze_video_missing_file():
    """Test analisi video senza file"""
    response = client.post("/analyze/video")
    assert response.status_code == 422  # Missing file 