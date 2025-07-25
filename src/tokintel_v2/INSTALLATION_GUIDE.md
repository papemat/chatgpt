# [INFO] TokIntel v2.1 - Guida di Installazione Enterprise

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

## ⚙️ Configurazione Manuale

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

## 🎯 Caratteristiche Enterprise

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
