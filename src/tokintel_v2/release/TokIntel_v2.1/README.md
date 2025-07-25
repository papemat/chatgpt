# [REPORT] TokIntel v2.1 - Analizzatore Video TikTok

> **Analizzatore modulare e scalabile per video TikTok con architettura AI avanzata - Enterprise Grade**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Audit](https://img.shields.io/badge/Audit-PASSED-brightgreen.svg)](https://github.com/yourusername/tokintel-v2/actions)
[![Type Check](https://img.shields.io/badge/Type%20Check-PASSED-brightgreen.svg)](https://github.com/yourusername/tokintel-v2/actions)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-ACTIVE-brightgreen.svg)](https://github.com/yourusername/tokintel-v2/actions)
[![Version](https://img.shields.io/badge/Version-2.1.0-orange.svg)](VERSION.txt)

## 🎯 Panoramica

TokIntel v2 è un sistema avanzato per l'analisi automatica di video TikTok che combina:

- **🎥 Estrazione frame intelligente** con OpenCV
- **🎤 Trascrizione audio** con Whisper
- **👁️ Riconoscimento testo** con OCR
- **[INFO] Analisi semantica** con LLM (GPT-4, locali)
- **[REPORT] Scoring automatico** per engagement e viralità
- **[INFO] Interfaccia web** con Streamlit

## ✨ Caratteristiche Principali

### [INFO] Architettura Modulare
- **Separazione delle responsabilità** tra scraping, analisi, UI e configurazione
- **Sistema di logging** centralizzato e configurabile
- **Gestione configurazioni** con validazione Pydantic
- **Supporto per modelli locali e remoti** (OpenAI, LM Studio, Ollama)

### [REPORT] Analisi Avanzata
- **Estrazione frame asincrona** con retry logic
- **Analisi engagement** multi-dimensionale
- **Scoring viralità** basato su keywords e tendenze
- **Suggerimenti ottimizzazione** automatici
- **Analisi target audience** dettagliata

### [INFO] Interfaccia Utente
- **Dashboard Streamlit** responsive e moderna
- **Visualizzazioni interattive** con Plotly
- **Upload drag & drop** per video
- **Esportazione multipla** (JSON, CSV, PDF)
- **Configurazione avanzata** tramite sidebar

## [INFO] Installazione

### Prerequisiti

- Python 3.8+
- FFmpeg (per elaborazione video)
- Modello LLM (OpenAI API key o locale)

### Installazione Rapida

```bash
# Clona il repository
git clone https://github.com/yourusername/tokintel-v2.git
cd tokintel-v2

# Installa le dipendenze
pip install -r requirements.txt

# Configura le variabili d'ambiente
cp config.yaml.example config.yaml
# Modifica config.yaml con le tue impostazioni
```

### Dipendenze Principali

```bash
# Core dependencies
pip install opencv-python streamlit pydantic pyyaml

# AI/ML dependencies
pip install openai whisper transformers torch

# UI dependencies
pip install plotly pandas numpy

# Optional: per modelli locali
pip install ollama lmstudio
```

## ⚙️ Configurazione

### File di Configurazione

Il file `config.yaml` contiene tutte le impostazioni:

```yaml
# Basic settings
model: "gpt-4"
language: "it"

# Analysis keywords
keywords:
  - "motivazione"
  - "hook"
  - "viral"
  - "emozione"

# LLM configuration
llm_config:
  model: "gpt-4"
  endpoint: null  # Per modelli locali
  api_key: null   # OpenAI API key
  timeout: 30
  max_retries: 3
  temperature: 0.7
  max_tokens: 500

# Processing settings
frame_extraction_interval: 30
max_video_duration: 300
```

### Variabili d'Ambiente

Puoi sovrascrivere le configurazioni con variabili d'ambiente:

```bash
export TOKINTEL_MODEL="gpt-3.5-turbo"
export TOKINTEL_LANGUAGE="en"
export TOKINTEL_LLM_API_KEY="your-openai-key"
export TOKINTEL_LLM_ENDPOINT="http://localhost:1234"
```

## 🎮 Utilizzo

### Interfaccia Web (Raccomandato)

```bash
# Avvia l'interfaccia Streamlit
python main.py --ui

# Oppure direttamente
streamlit run ui/interface.py
```

### Linea di Comando

```bash
# Analizza un singolo video
python main.py --input video.mp4

# Analizza una directory
python main.py --input /path/to/videos/

# Con configurazione personalizzata
python main.py --input video.mp4 --config custom_config.yaml

# Modalità verbose
python main.py --input video.mp4 --verbose
```

### Programmatico

```python
from main import TokIntelCore

# Inizializza il core
core = TokIntelCore("config/config.yaml")

# Analizza un video
results = await core.process_video("video.mp4")

# Analizza una directory
results = core.run_sync("/path/to/videos/")
```

## [INFO] Struttura del Progetto

```
TokIntel_v2/
├── [INFO] agent/                 # Agenti di elaborazione
│   ├── scraper.py           # Estrazione frame
│   ├── audio.py             # Trascrizione audio
│   ├── vision.py            # Analisi visiva
│   ├── synthesis.py         # Sintesi LLM
│   └── scoring.py           # Scoring automatico
├── [INFO] core/                 # Core del sistema
│   ├── config.py            # Gestione configurazioni
│   ├── logger.py            # Sistema di logging
│   └── exceptions.py        # Gestione errori
├── [INFO] llm/                  # Gestione LLM
│   ├── handler.py           # Handler centralizzato
│   └── prompts.py           # Template prompt
├── [INFO] ui/                   # Interfaccia utente
│   ├── interface.py         # Dashboard Streamlit
│   └── streamlit_launcher.py
├── [INFO] utils/                # Utility
│   └── file_utils.py        # Gestione file
├── [INFO] tests/                # Test unitari
├── [INFO] config/               # Configurazioni
├── [INFO] output/               # Risultati
├── main.py                  # Entry point
└── config.yaml              # Configurazione principale
```

## [INFO] Moduli Principali

### 🎥 ScraperAgent
- Estrazione frame asincrona con OpenCV
- Retry logic e gestione errori
- Supporto per batch processing
- Logging dettagliato delle operazioni

### [INFO] SynthesisAgent
- Integrazione con LLM (OpenAI e locali)
- Template prompt centralizzati
- Analisi engagement e viralità
- Timing e performance tracking

### ⚙️ ConfigManager
- Validazione Pydantic delle configurazioni
- Supporto variabili d'ambiente
- Merge configurazioni file/env
- Validazione automatica

### [INFO] StreamlitInterface
- Dashboard responsive e moderna
- Upload drag & drop
- Visualizzazioni interattive
- Configurazione avanzata

## [INFO] Testing

```bash
# Installa pytest
pip install pytest pytest-asyncio

# Esegui tutti i test
pytest tests/

# Test specifici
pytest tests/test_config.py
pytest tests/test_prompts.py

# Con coverage
pytest --cov=. tests/
```

## [REPORT] Output e Risultati

### Formato Risultati

```json
{
  "summary": "Sintesi del contenuto video...",
  "score": {
    "overall": 8.5,
    "engagement": 7.2,
    "viral_potential": 8.8,
    "keywords_match": 6.5
  },
  "details": {
    "transcript": "Trascrizione audio...",
    "ocr_text": "Testo rilevato...",
    "matched_keywords": ["motivazione", "hook"],
    "suggestions": ["Miglioramenti suggeriti..."]
  },
  "metadata": {
    "processing_time": 45.2,
    "frames_analyzed": 120,
    "model_used": "gpt-4"
  }
}
```

### Formati di Esportazione

- **JSON**: Dati completi strutturati
- **CSV**: Tabella con metriche principali
- **PDF**: Report formattato
- **TXT**: Sintesi testuale

## [INFO] Configurazione Avanzata

### Modelli Locali

```yaml
llm_config:
  model: "llama2"
  endpoint: "http://localhost:11434"  # Ollama
  # oppure
  endpoint: "http://localhost:1234"   # LM Studio
```

### Personalizzazione Prompt

```python
from llm.prompts import PromptTemplates

# Prompt personalizzato
custom_prompt = PromptTemplates.build_summary_prompt(
    transcript="...",
    ocr_text="...",
    custom_instructions="Analisi specifica per..."
)
```

### Logging Avanzato

```yaml
log_level: "DEBUG"
log_file: "logs/tokintel.log"
```

## 🚨 Risoluzione Problemi

### Errori Comuni

1. **FFmpeg non trovato**
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Scarica da https://ffmpeg.org/download.html
   ```

2. **OpenAI API Key mancante**
   ```bash
   export TOKINTEL_LLM_API_KEY="your-key-here"
   ```

3. **Memoria insufficiente**
   - Riduci `frame_extraction_interval`
   - Usa modelli più piccoli
   - Aumenta `max_video_duration`

### Debug

```bash
# Modalità verbose
python main.py --input video.mp4 --verbose

# Log dettagliato
export TOKINTEL_LOG_LEVEL="DEBUG"
```

## 🤝 Contribuire

1. Fork il progetto
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

### Linee Guida

- Segui PEP 8 per il codice Python
- Aggiungi test per nuove funzionalità
- Aggiorna la documentazione
- Usa type hints

## [INFO] Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙏 Ringraziamenti

- **OpenAI** per GPT-4 e Whisper
- **Streamlit** per l'interfaccia web
- **OpenCV** per l'elaborazione video
- **Pydantic** per la validazione dati

## [INFO] Supporto

- [INFO] Email: support@tokintel.com
- 💬 Discord: [TokIntel Community](https://discord.gg/tokintel)
- [INFO] Wiki: [Documentazione completa](https://wiki.tokintel.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/tokintel-v2/issues)

---

**TokIntel v2** - Trasforma i tuoi video TikTok in insights strategici! [INFO] 