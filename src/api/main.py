from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import export_csv, download_file, export_pdf, export_excel, export_bundle
import os

app = FastAPI(title="TokIntel API", version="0.1")

# CORS (puoi limitarlo se servisse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi router
app.include_router(export_csv.router)
app.include_router(download_file.router)
app.include_router(export_pdf.router)
app.include_router(export_excel.router)
app.include_router(export_bundle.router)

# Cartella di download
os.makedirs("src/api/downloads", exist_ok=True) 