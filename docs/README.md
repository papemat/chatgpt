# TokIntel v2

[![version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./CHANGELOG.md) [![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE) [![tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](./)

TokIntel v2 è una piattaforma avanzata per l'analisi di video TikTok tramite AI, con interfaccia Streamlit, pipeline automatizzata, supporto multi-agente e compatibilità cross-platform (Windows/Linux/Mac).

## Caratteristiche principali
- Analisi automatica video TikTok
- Interfaccia utente Streamlit professionale
- Chat con agenti AI specializzati
- Pipeline di analisi e reportistica
- Compatibilità Windows, Linux, Mac
- Docker supportato
- Test automatici inclusi

## Installazione

### Requisiti
- Python 3.8+
- pip

### Installazione standard
```bash
pip install .
```

### Avvio interfaccia
```bash
python -m TokIntel_v2.ui.streamlit_launcher
```

### Docker
Costruisci e avvia con Docker Compose:
```bash
docker-compose up --build
```

## Testing
Esegui i test automatici:
```bash
pytest
```

## Badge
- Versione: 2.0.0
- Licenza: MIT
- Test: passing

## Note
- Per funzionalità Pro, installa anche i requirements aggiuntivi (`requirements_pro.txt`).
- Per problemi di compatibilità, assicurati che la console supporti caratteri ASCII.

## Licenza
MIT 

## 📤 Funzioni di Esportazione

TokIntel supporta l’esportazione dei dati analizzati in più formati:

- **CSV** (`.csv`) – compatibile con Excel/Sheets
- **PDF** (`.pdf`) – report leggibile stampabile
- **Excel** (`.xlsx`) – esportazione strutturata con colori e formattazione
- **Bundle ZIP** (`.zip`) – contenente CSV, PDF, Excel, README e metadati

### 📦 Esportazione completa via UI

Nella UI Streamlit troverai:

- 📄 Pulsante “Esporta CSV”
- 🧾 Pulsante “Esporta PDF”
- 📊 Pulsante “Esporta Excel”
- 📦 Pulsante **“Esporta Tutto (ZIP)”** → genera automaticamente un bundle `tokintel_export_<timestamp>.zip` pronto al download

### 📁 Output ZIP contiene:

```
tokintel_export_20250725_XXXX/
├── export.csv
├── export.pdf
├── export.xlsx
├── README.txt
├── metadata.json
```

--- 