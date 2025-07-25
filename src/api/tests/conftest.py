import pytest
from fastapi.testclient import TestClient
from api.main import app
import shutil
import os

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True, scope="function")
def cleanup_downloads():
    yield
    downloads_dir = "src/api/downloads"
    for f in os.listdir(downloads_dir):
        if f.startswith("export_") or f.startswith("tokintel_bundle_") or f.startswith("metadata_") or f == "README.txt":
            try:
                os.remove(os.path.join(downloads_dir, f))
            except Exception:
                pass 