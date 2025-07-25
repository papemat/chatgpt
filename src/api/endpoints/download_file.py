from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["Download"])

DOWNLOAD_DIR = "src/api/downloads"

@router.get("/downloads/{filename}", summary="Scarica un file esportato", response_description="File binario da scaricare")
def download_file(filename: str):
    """
    Scarica un file precedentemente esportato (CSV, PDF, Excel, ZIP).
    - **filename**: nome del file da scaricare
    """
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File non trovato.")

    return FileResponse(filepath, media_type='application/octet-stream', filename=filename) 