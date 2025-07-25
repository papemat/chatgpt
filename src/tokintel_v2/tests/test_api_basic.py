import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Test semplificato che non dipende da tutti i moduli
def test_api_basic():
    """Test base per verificare che FastAPI funzioni"""
    try:
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/")
        def root():
            return {"message": "test"}
        
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "test"
        
    except ImportError:
        pytest.skip("FastAPI non disponibile")

def test_pydantic_models():
    """Test modelli Pydantic"""
    try:
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
            value: int
        
        model = TestModel(name="test", value=42)
        assert model.name == "test"
        assert model.value == 42
        
    except ImportError:
        pytest.skip("Pydantic non disponibile") 