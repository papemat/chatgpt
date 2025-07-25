from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import uuid
from ..utils.io_helpers import export_to_excel

class ExportExcelRequest(BaseModel):
    """Richiesta per esportazione Excel. I dati devono essere una lista di dict."""
    data: List[Dict]

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

@router.post("/excel", summary="Esporta dati in Excel", response_description="Nome file Excel e URL di download")
def export_excel(request: ExportExcelRequest):
    """
    Esporta i dati forniti in un file Excel e restituisce il nome del file e l'URL di download.
    - **data**: lista di dizionari da esportare
    """
    data_list = request.data
    uid = uuid.uuid4().hex[:6]
    filename = f"export_{uid}.xlsx"
    out_dir = os.getenv("EXPORT_DIR", "src/api/downloads")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    try:
        export_to_excel(data_list, filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'esportazione Excel: {e}")
    return {
        "filename": filename,
        "download_url": f"/downloads/{filename}"
    } 