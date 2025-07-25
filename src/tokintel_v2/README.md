[![CI](https://github.com/TUO_USERNAME/TUO_REPO/actions/workflows/tests.yml/badge.svg)](https://github.com/TUO_USERNAME/TUO_REPO/actions)
[![codecov](https://codecov.io/gh/TUO_USERNAME/TUO_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/TUO_USERNAME/TUO_REPO)
[![PyPI version](https://img.shields.io/pypi/v/tokintel.svg)](https://pypi.org/project/tokintel/)

# DONE: README.md aggiornato con istruzioni test/linting/refactor

# 🎯 TokIntel v2 - Analizzatore Video TikTok

[![PyPI - CLI Ready](https://img.shields.io/badge/CLI-tokintel-blue?logo=python&label=tokintel%20CLI)](https://pypi.org/project/tokintel/)
[![PyPI - pip install .](https://img.shields.io/badge/pip%20install-.--success?logo=pypi)](https://pypi.org/project/tokintel/)

**Analizzatore modulare di video TikTok con architettura scalabile e automazione completa.**

## [INFO] Caratteristiche Principali

- **[REPORT] Analisi Video Avanzata**: Estrazione frame, analisi contenuto, metriche performance
- **🤖 AI Integration**: Integrazione con modelli AI per analisi semantica
- **💾 Database PostgreSQL**: Sistema di storage robusto con SQLAlchemy
- **🕷️ Scraping TikTok**: Download automatico video e metadati
- **⏰ Scheduler Automatico**: Analisi batch programmata
- **[INFO] UI Streamlit**: Interfaccia web moderna e intuitiva
- **[REPORT] Analytics Dashboard**: Trend, insights e reportistica
- **[INFO] Automazione Completa**: Test, linting, type checking automatici

## [INFO] Installazione

### Via pip
```bash
pip install tokintel
```

### Via pipx (consigliato)
```bash
pipx install git+https://github.com/TUO_USERNAME/TUO_REPO.git
```
> [INFO] Assicurati di avere `pipx` installato e il PATH configurato

## [INFO] Installazione

### Prerequisiti

- Python 3.8+
- PostgreSQL (opzionale, SQLite per sviluppo)
- Playwright per scraping

### Installazione Base

```bash
# Clone del repository
git clone https://github.com/your-org/tokintel-v2.git
cd tokintel-v2

# Ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate     # Windows

# Dipendenze base
pip install -r requirements.txt

# Dipendenze sviluppo (opzionale)
pip install -r requirements-dev.txt
```

### Configurazione

1. **Database**: Configura PostgreSQL o usa SQLite per sviluppo
2. **Playwright**: Installa browser per scraping
   ```bash
   playwright install chromium
   ```
3. **Configurazione**: Copia e modifica `config/config.yaml.example`

## [INFO] Testing e Qualità Codice

### Test Automatici

```bash
# Esegui tutti i test
python scripts/run_tests.py

# Solo test unitari
python scripts/run_tests.py --unit-only

# Solo test di integrazione
python scripts/run_tests.py --integration-only

# Test con coverage
python scripts/run_tests.py --no-linting --no-type-checking
```

### Linting e Type Checking

```bash
# Formattazione codice
black .

# Ordinamento import
isort .

# Linting
flake8 .

# Type checking
mypy .

# Tutto insieme
python scripts/run_tests.py --no-coverage
```

### Pre-commit Hooks

```bash
# Installa pre-commit hooks
pre-commit install

# Esegui manualmente
pre-commit run --all-files
```

## [INFO] Sviluppo

### Struttura Progetto

```
TokIntel_v2/
├── [INFO] core/           # Funzionalità core
├── [INFO] db/            # Database e modelli
├── [INFO] scraper/       # Scraping TikTok
├── [INFO] analytics/     # Analisi dati
├── [INFO] ui/            # Interfacce Streamlit
├── [INFO] scheduler/     # Scheduler automatico
├── [INFO] scripts/       # Script di utilità
├── [INFO] tests/         # Test unitari e integrazione
├── [INFO] config/        # Configurazioni
└── [INFO] tools/         # Tool di sviluppo
```

### Workflow Sviluppo

1. **Setup ambiente**:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

2. **Sviluppo**:
   ```bash
   # Codifica con validazione automatica
   git add .
   git commit -m "feat: nuova funzionalità"
   ```

3. **Test**:
   ```bash
   # Test completi
   python scripts/run_tests.py
   
   # Coverage report
   open coverage_html/index.html
   ```

### Refactor e Utilities

```bash
# Genera report refactor
python scripts/refactor_utils.py --generate-report

# Aggiorna TODO
python scripts/refactor_utils.py --update-todo

# Scansiona commenti # DONE:
python scripts/refactor_utils.py --scan-done

# Converti JSON in Markdown
python scripts/refactor_utils.py --json-to-md file.json
```

## [INFO] Utilizzo

### Installazione come CLI

```bash
pip install .
```

### Esempio di utilizzo CLI

```bash
# Analizza un video
$ tokintel analyze sample.mp4

# Avvia la dashboard
$ tokintel dashboard

# Avvia la UI Streamlit
$ tokintel ui

# Help
$ tokintel --help

# Fallback: avvio tramite modulo
$ python -m tokintel analyze sample.mp4
```

### Interfaccia Web

```bash
# Avvia Streamlit
streamlit run ui/interface.py

# Dashboard Pro
streamlit run ui/pro_dashboard.py

# Libreria TikTok
streamlit run ui/tiktok_library.py
```

### CLI

```bash
# Analisi singolo video
python main.py --video path/to/video.mp4

# Scheduler automatico
python scheduler/auto_scheduler.py --user-id 1 --interval 60

# Batch analysis
python batch_auto_analyze.py --user-id 1
```

### API

```python
from core import TokIntelCore

# Inizializza
core = TokIntelCore()

# Analizza video
results = await core.analyze_video("video.mp4")
print(f"Score: {results['overall_score']}")
```

## [REPORT] Dashboard e Analytics

### Metriche Principali

- **Overall Score**: Punteggio complessivo del video
- **Engagement Rate**: Tasso di engagement previsto
- **Viral Potential**: Potenziale virale
- **Content Quality**: Qualità del contenuto
- **Trend Analysis**: Analisi trend temporali

### Insights Disponibili

- **Keywords**: Parole chiave estratte
- **Emotions**: Analisi emozionale
- **Themes**: Temi del contenuto
- **Recommendations**: Suggerimenti di miglioramento
- **Competitive Analysis**: Analisi competitiva

## [INFO] Configurazione Avanzata

### Database

```yaml
# config/config.yaml
database:
  type: postgresql  # o sqlite
  host: localhost
  port: 5432
  name: tokintel
  user: postgres
  password: your_password
```

### AI Models

```yaml
ai:
  provider: openai  # o local
  model: gpt-4
  api_key: your_api_key
  temperature: 0.7
```

### Scheduler

```yaml
scheduler:
  enabled: true
  interval_minutes: 60
  max_concurrent_jobs: 5
  retry_attempts: 3
```

## [INFO] Testing

### Test Unitari

```bash
# Esegui test specifici
pytest tests/test_database.py -v

# Test con coverage
pytest --cov=. --cov-report=html

# Test paralleli
pytest -n auto
```

### Test di Integrazione

```bash
# Test database
pytest tests/test_database_integration.py

# Test scraper
pytest tests/test_scraper_integration.py

# Test UI
pytest tests/test_ui_integration.py
```

### Test Performance

```bash
# Profiling
python -m cProfile -o profile.stats main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

## [REPORT] Monitoraggio

### Logs

```bash
# Log di sistema
tail -f logs/tokintel.log

# Log scheduler
tail -f logs/scheduler.log

# Log scraping
tail -f logs/scraper.log
```

### Metriche

```python
from analytics.dashboard import get_analytics_summary

# Statistiche generali
stats = get_analytics_summary(user_id=1, days=30)
print(f"Video analizzati: {stats['total_analyses']}")
```

## [INFO] Sicurezza

### Best Practices

- [OK] Validazione input in tutti i moduli
- [OK] Gestione errori granulare
- [OK] Logging strutturato
- [OK] Type checking completo
- [OK] Linting automatico
- [OK] Test di sicurezza con Bandit

### Configurazione Sicurezza

```yaml
security:
  input_validation: true
  sql_injection_protection: true
  xss_protection: true
  rate_limiting: true
  max_file_size: 100MB
```

## 🤝 Contribuire

### Setup Sviluppo

1. **Fork** del repository
2. **Clone** del fork
3. **Branch** per feature: `git checkout -b feature/nuova-funzionalita`
4. **Commit** con standard: `git commit -m "feat: descrizione"`
5. **Push** e **Pull Request**

### Standard di Codice

- **Black** per formattazione
- **isort** per ordinamento import
- **flake8** per linting
- **mypy** per type checking
- **Docstring** Google-style
- **Test** per tutte le funzionalità

### Checklist PR

- [ ] Codice formattato con Black
- [ ] Import ordinati con isort
- [ ] Linting passa con flake8
- [ ] Type checking passa con mypy
- [ ] Test unitari aggiunti
- [ ] Test di integrazione aggiunti
- [ ] Documentazione aggiornata
- [ ] Pre-commit hooks passano

## 📤 Esportazione dei dati

TokIntel consente di esportare i risultati delle analisi in quattro formati:

- **CSV** (`.csv`): per utilizzo in Excel, Google Sheets, analisi dati
- **PDF** (`.pdf`): per generare un report leggibile e stampabile
- **Excel** (`.xlsx`): per analisi avanzate con formattazione
- **ZIP** (`.zip`): pacchetto completo con tutti i formati

Le funzioni sono disponibili nel modulo `extensions/export_tools.py`:
- `export_to_csv(data, filepath)`
- `export_to_pdf(data, filepath)`
- `export_to_excel(data, filepath)`
- `export_to_zip(data, output_dir)`

La UI Streamlit include i pulsanti:
- 📄 **Esporta CSV**
- 🧾 **Esporta PDF**
- 📊 **Esporta Excel**
- 📦 **Esporta tutto (ZIP)**

I file possono essere scaricati direttamente dall'interfaccia.

### Esempio di utilizzo

```python
from extensions import export_tools

# Esporta dati in CSV
dati_csv = [
    {"Video": "TikTok1", "Autore": "User123", "Sentiment": "Positivo"},
    {"Video": "TikTok2", "Autore": "User456", "Sentiment": "Neutro"}
]
export_tools.export_to_csv(dati_csv, "risultati.csv")

# Esporta dati in PDF
dati_pdf = {
    "Analisi": "TikTok1",
    "Contenuto": "Tratta di IA e tool utili",
    "Sentiment": "Positivo",
    "Tags": "AI, productivity"
}
export_tools.export_to_pdf(dati_pdf, "report.pdf")

# Esporta dati in Excel
export_tools.export_to_excel(dati_csv, "risultati.xlsx")

# Esporta tutto in ZIP
zip_data = {
    'csv_data': dati_csv,
    'json_data': dati_pdf
}
zip_path = export_tools.export_to_zip(zip_data, "exports/")
```

## [INFO] Licenza

MIT License - vedi [LICENSE](LICENSE) per dettagli.

## 🆘 Supporto

- **Documentazione**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/tokintel-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/tokintel-v2/discussions)
- **Email**: team@tokintel.com

---

TokIntel v2.0.0 è pubblica, stabile, documentata e deployabile ovunque.

## [INFO] Coverage

Per abilitare il badge di coverage, registra il repo su https://codecov.io e aggiungi il token `CODECOV_TOKEN` nei Secrets GitHub. 

## [INFO] Deploy & Demo

TokIntel v2 is designed for universal deployment and quick testing. You can run it locally, in the cloud, or via container with minimal setup.

### 🐳 Docker

Build and run the UI and CLI with Docker Compose:

```bash
docker-compose up
```
- The UI will be available at [http://localhost:8501](http://localhost:8501)
- CLI example: `tokintel analyze sample.mp4`

### [INFO] Google Colab

Try the interactive demo notebook:
- [TokIntel_Colab_Demo.ipynb](TokIntel_Colab_Demo.ipynb)

> The Colab notebook simulates the full analysis pipeline, even if Ollama/Whisper are not available on Colab. For full features, run locally.

### 🖥️ Local (pip/pipx)

Install and run locally:
```bash
pip install tokintel
# or
pipx install git+https://github.com/TUO_USERNAME/TUO_REPO.git
```

### [INFO] Streamlit UI

Launch the web interface:
```bash
streamlit run ui/interface.py
```

### ☁️ Heroku/Cloud

You can deploy the Streamlit UI or API to Heroku or any cloud provider supporting Python and Docker. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

### 🤖 HuggingFace Spaces (coming soon)

A public demo will be available on HuggingFace Spaces.

---

## 🏷️ Badges & Links

[![CI](https://github.com/TUO_USERNAME/TUO_REPO/actions/workflows/tests.yml/badge.svg)](https://github.com/TUO_USERNAME/TUO_REPO/actions)
[![codecov](https://codecov.io/gh/TUO_USERNAME/TUO_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/TUO_USERNAME/TUO_REPO)
[![PyPI version](https://img.shields.io/pypi/v/tokintel.svg)](https://pypi.org/project/tokintel/)
[![Colab Demo](https://colab.research.google.com/assets/colab-badge.svg)](TokIntel_Colab_Demo.ipynb)

- **PyPI:** [https://pypi.org/project/tokintel/](https://pypi.org/project/tokintel/)
- **Colab Demo:** [TokIntel_Colab_Demo.ipynb](TokIntel_Colab_Demo.ipynb)
- **Streamlit Demo:** [http://localhost:8501](http://localhost:8501) (local)
- **DockerHub:** (coming soon)
- **HuggingFace Spaces:** (coming soon)

## 🏷 Versionamento automatico

Gestisci facilmente le versioni e il changelog:

```bash
# Mostra la versione attuale
python scripts/version.py --version

# Bump patch (es: 2.0.0 → 2.0.1)
python scripts/version.py --bump patch

# Bump minor (es: 2.0.1 → 2.1.0)
python scripts/version.py --bump minor

# Imposta una versione specifica
python scripts/version.py --set 2.2.0

# Bump e crea tag git
python scripts/version.py --bump patch --tag
``` 