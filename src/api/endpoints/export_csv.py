from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import csv, uuid, os

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

DOWNLOAD_DIR = "src/api/downloads"

class ExportCSVRequest(BaseModel):
    """Richiesta per esportazione CSV. I dati devono essere una lista di dict."""
    data: List[Dict]

@router.post("/csv", summary="Esporta dati in CSV", response_description="Nome file CSV e URL di download")
def export_csv(request: ExportCSVRequest):
    """
    Esporta i dati forniti in un file CSV e restituisce il nome del file e l'URL di download.
    - **data**: lista di dizionari da esportare
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="Dati CSV mancanti.")

    filename = f"export_{uuid.uuid4().hex}.csv"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        with open(filepath, mode="w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=request.data[0].keys())
            writer.writeheader()
            writer.writerows(request.data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'esportazione: {str(e)}")

    return {"filename": filename, "download_url": f"/downloads/{filename}"} 