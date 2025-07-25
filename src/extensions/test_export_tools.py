"""
Test unitari per il modulo export_tools.py
Autore: Matteo Papetti
Progetto: TokIntel v2 Extensions
"""

import os
import pytest
import sys
import zipfile
from pathlib import Path

# Aggiungi il percorso delle extensions al path
sys.path.append(str(Path(__file__).parent))

from export_tools import export_to_csv, export_to_pdf, export_to_excel, export_to_zip, export_bundle

# --- Setup dati di test ---
csv_data = [
    {"Nome": "Alice", "Età": 30, "Città": "Roma"},
    {"Nome": "Bob", "Età": 25, "Città": "Milano"},
    {"Nome": "Charlie", "Età": 35, "Città": "Napoli"}
]

pdf_data = {
    "Titolo": "Analisi TokIntel",
    "Risultato": "Positivo",
    "Autore": "TokIntel v2",
    "Data": "2024-01-15",
    "Punteggio": "85/100"
}

# --- Percorsi di test ---
csv_path = "test_export.csv"
pdf_path = "test_export.pdf"
excel_path = "test_export.xlsx"
zip_path = "test_export.zip"

class TestExportTools:
    """Classe di test per le funzioni di esportazione"""
    
    def test_export_to_csv_crea_file(self):
        """Test: verifica che export_to_csv crei un file valido"""
        try:
            export_to_csv(csv_data, csv_path)
            assert os.path.exists(csv_path), "File CSV non creato"
            
            # Verifica contenuto
            with open(csv_path, "r", encoding="utf-8") as f:
                contenuto = f.read()
                assert "Alice" in contenuto, "Dati Alice non trovati"
                assert "Bob" in contenuto, "Dati Bob non trovati"
                assert "Charlie" in contenuto, "Dati Charlie non trovati"
                assert "Nome,Età,Città" in contenuto, "Header CSV mancante"
                
        finally:
            # Pulizia
            if os.path.exists(csv_path):
                os.remove(csv_path)
    
    def test_export_to_pdf_crea_file(self):
        """Test: verifica che export_to_pdf crei un file valido"""
        try:
            export_to_pdf(pdf_data, pdf_path)
            assert os.path.exists(pdf_path), "File PDF non creato"
            assert os.path.getsize(pdf_path) > 0, "File PDF vuoto"
            
        finally:
            # Pulizia
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    def test_export_to_csv_dati_vuoti(self):
        """Test: verifica che export_to_csv gestisca dati vuoti"""
        with pytest.raises(ValueError, match="Dati vuoti"):
            export_to_csv([], csv_path)
    
    def test_export_to_csv_dati_none(self):
        """Test: verifica che export_to_csv gestisca dati None"""
        with pytest.raises(ValueError, match="Dati vuoti"):
            export_to_csv(None, csv_path)
    
    def test_export_to_csv_formato_corretto(self):
        """Test: verifica che il CSV abbia il formato corretto"""
        try:
            export_to_csv(csv_data, csv_path)
            
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            # Verifica header
            assert lines[0].strip() == "Nome,Età,Città", "Header CSV errato"
            
            # Verifica numero righe (header + 3 dati)
            assert len(lines) == 4, f"Numero righe errato: {len(lines)}"
            
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)
    
    def test_export_to_excel_crea_file(self):
        """Test: verifica che export_to_excel crei un file valido"""
        try:
            export_to_excel(csv_data, excel_path)
            assert os.path.exists(excel_path), "File Excel non creato"
            assert os.path.getsize(excel_path) > 0, "File Excel vuoto"
            
        finally:
            if os.path.exists(excel_path):
                os.remove(excel_path)
    
    def test_export_to_excel_dati_vuoti(self):
        """Test: verifica che export_to_excel gestisca dati vuoti"""
        with pytest.raises(ValueError, match="Dati vuoti"):
            export_to_excel([], excel_path)
    
    def test_export_to_zip_crea_file(self):
        """Test: verifica che export_to_zip crei un file valido"""
        try:
            zip_data = {
                'csv_data': csv_data,
                'json_data': pdf_data
            }
            result_path = export_to_zip(zip_data, ".")
            assert os.path.exists(result_path), "File ZIP non creato"
            assert os.path.getsize(result_path) > 0, "File ZIP vuoto"
            
            # Verifica contenuto ZIP
            with zipfile.ZipFile(result_path, 'r') as zipf:
                file_list = zipf.namelist()
                assert 'export.csv' in file_list, "CSV non presente nel ZIP"
                assert 'export.json' in file_list, "JSON non presente nel ZIP"
                assert 'metadata.json' in file_list, "Metadata non presente nel ZIP"
                assert 'README.txt' in file_list, "README non presente nel ZIP"
            
        finally:
            if os.path.exists(zip_path):
                os.remove(zip_path)
            # Rimuovi anche il file ZIP con timestamp
            for f in os.listdir("."):
                if f.startswith("tokintel_export_") and f.endswith(".zip"):
                    os.remove(f)
    
    def test_export_bundle_crea_file(self):
        """Test: verifica che export_bundle crei un file valido"""
        try:
            bundle_data = {
                'csv_data': csv_data,
                'json_data': pdf_data
            }
            result_path = export_bundle(bundle_data, ".")
            assert os.path.exists(result_path), "File bundle ZIP non creato"
            assert os.path.getsize(result_path) > 0, "File bundle ZIP vuoto"
            
        finally:
            # Rimuovi file bundle con timestamp
            for f in os.listdir("."):
                if f.startswith("tokintel_export_") and f.endswith(".zip"):
                    os.remove(f)
                if f.startswith("tokintel_bundle_"):
                    if os.path.isdir(f):
                        import shutil
                        shutil.rmtree(f)

if __name__ == "__main__":
    # Esegui i test se chiamato direttamente
    pytest.main([__file__, "-v"]) 