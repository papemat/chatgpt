#!/usr/bin/env python3
"""
TokIntel v2.1 - Create Release ZIP
Script per creare il pacchetto ZIP finale del rilascio
"""

from typing import Dict, List, Any, Optional
import os
import zipfile
from datetime import datetime
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def create_release_zip():
    """Crea il ZIP finale del rilascio"""
    
    # Percorsi
    project_root = Path(__file__).parent
    release_dir = project_root / "release" / "TokIntel_v2.1"
    zip_name = f"TokIntel_v2.1_Enterprise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = project_root / zip_name
    
    logger.info(f"[INFO] Creazione ZIP: {zip_name}")
    
    # Verifica che la directory release esista
    if not release_dir.exists():
        logger.info("[ERROR] Directory release non trovata. Esegui prima final_release_prep.py")
        return False
    
    # Crea il ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Aggiungi tutti i file dalla directory release
        for file_path in release_dir.rglob('*'):
            if file_path.is_file():
                # Calcola il path relativo nel ZIP
                arcname = file_path.relative_to(release_dir)
                zipf.write(file_path, arcname)
                logger.info(f"[REPORT] Aggiunto: {arcname}")
    
    logger.info(f"[OK] ZIP creato: {zip_path}")
    logger.info(f"[REPORT] Dimensione: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    
    return True


def create_installation_guide():
    """Crea guida di installazione"""
    
    guide = """# [INFO] TokIntel v2.1 - Guida di Installazione Enterprise

## [INFO] Prerequisiti

- **Python 3.8+** installato
- **FFmpeg** per elaborazione video
- **Git** (opzionale, per versioning)

## [INFO] Installazione Rapida

### 1. Estrazione
```bash
unzip TokIntel_v2.1_Enterprise_*.zip
cd TokIntel_v2.1
```

### 2. Installazione Automatica
```bash
# Linux/macOS
chmod +x install.sh run.sh
./install.sh

# Windows
install.sh
```

### 3. Configurazione
```bash
# Copia configurazione di esempio
cp config.yaml.example config.yaml

# Modifica config.yaml con le tue impostazioni
nano config.yaml
```

### 4. Avvio
```bash
# Linux/macOS
./run.sh

# Windows
run.sh
```

## [INFO] Configurazione Manuale

### Dipendenze Python
```bash
pip install -r requirements.txt
```

### Configurazione OpenAI
```yaml
# config.yaml
openai:
  api_key: "your-openai-api-key"
  model: "gpt-4"
```

### Configurazione Modelli Locali
```yaml
# config.yaml
local_models:
  endpoint: "http://localhost:1234/v1"
  model: "llama2"
```

## [INFO] Test

```bash
# Test suite completa
pytest tests/ -v

# Test specifici
pytest tests/test_scoring.py -v
pytest tests/test_logger.py -v
```

## [REPORT] Verifica Installazione

1. **Avvia l'interfaccia**: `./run.sh`
2. **Apri browser**: http://localhost:8501
3. **Carica un video** di test
4. **Verifica analisi** completa

## [INFO] Risoluzione Problemi

### Errore: "No module named pytest"
```bash
pip install pytest pytest-cov
```

### Errore: "FFmpeg not found"
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Scarica da https://ffmpeg.org/download.html

### Errore: "OpenAI API key required"
```bash
# Aggiungi al config.yaml
openai:
  api_key: "your-api-key-here"
```

## [REPORT] CI/CD

Il progetto include GitHub Actions per:
- [OK] Code formatting (Black)
- [OK] Linting (Flake8)
- [OK] Type checking (MyPy)
- [OK] Unit testing (Pytest)
- [OK] Security scanning (Bandit)

## [INFO] Caratteristiche Enterprise

- **Audit Completo**: 121 issues risolti
- **Type Checking**: Validazione tipi completa
- **Test Suite**: Copertura critica
- **Documentazione**: Completa e aggiornata
- **Logging**: Strutturato e controllato
- **CI/CD**: Pipeline automatica

## [INFO] Supporto

- **Documentazione**: README.md
- **Report Audit**: post_audit_report.json
- **Configurazione**: config.yaml.example

---
*TokIntel v2.1 - Enterprise Grade Release*
"""
    
    # Salva guida
    guide_path = Path(__file__).parent / "INSTALLATION_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    logger.info(f"[INFO] Guida di installazione creata: {guide_path}")
    return True


def main():
    """Main function"""
    logger.info("[INFO] TokIntel v2.1 - Creazione ZIP Finale")
    
    # Crea ZIP
    if create_release_zip():
        logger.info("[OK] ZIP creato con successo")
    else:
        logger.info("[ERROR] Errore nella creazione ZIP")
        return
    
    # Crea guida installazione
    if create_installation_guide():
        logger.info("[OK] Guida installazione creata")
    else:
        logger.info("[ERROR] Errore nella creazione guida")
    
    logger.info("\n[INFO] Rilascio TokIntel v2.1 Enterprise completato!")
    logger.info("[INFO] ZIP disponibile nella root del progetto")
    logger.info("[INFO] Guida installazione: INSTALLATION_GUIDE.md")


if __name__ == "__main__":
    main() 