from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
import uuid
from ..utils.io_helpers import export_to_pdf

class ExportPDFRequest(BaseModel):
    """Richiesta per esportazione PDF. I dati devono essere un dizionario chiave:valore."""
    data: Dict

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

@router.post("/pdf", summary="Esporta dati in PDF", response_description="Nome file PDF e URL di download")
def export_pdf(request: ExportPDFRequest):
    """
    Esporta i dati forniti in un file PDF e restituisce il nome del file e l'URL di download.
    - **data**: dizionario chiave:valore da esportare
    """
    data_dict = request.data
    uid = uuid.uuid4().hex[:6]
    filename = f"export_{uid}.pdf"
    out_dir = os.getenv("EXPORT_DIR", "src/api/downloads")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    try:
        export_to_pdf(data_dict, filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'esportazione PDF: {e}")
    return {
        "filename": filename,
        "download_url": f"/downloads/{filename}"
    } 