from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import uuid
from ..utils.io_helpers import export_bundle

class ExportBundleRequest(BaseModel):
    """Richiesta per esportazione bundle ZIP. I dati devono essere una lista di dict."""
    data: List[Dict]

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

@router.post("/bundle", summary="Esporta dati in bundle ZIP", response_description="Nome file ZIP e URL di download")
def export_bundle_api(request: ExportBundleRequest):
    """
    Esporta i dati forniti in un bundle ZIP (CSV, PDF, Excel, README, metadata) e restituisce il nome del file e l'URL di download.
    - **data**: lista di dizionari da esportare
    """
    data_list = request.data
    uid = uuid.uuid4().hex[:6]
    filename = f"tokintel_bundle_{uid}.zip"
    out_dir = os.getenv("EXPORT_DIR", "src/api/downloads")
    os.makedirs(out_dir, exist_ok=True)
    bundle_path = os.path.join(out_dir, filename)
    try:
        export_bundle(data_list, bundle_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'esportazione bundle: {e}")
    return {
        "filename": filename,
        "download_url": f"/downloads/{filename}"
    } 