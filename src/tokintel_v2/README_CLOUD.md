# TokIntel v2.1 Cloud Deployment

## [INFO] Deploy su Cloud

TokIntel v2.1 supporta il deploy su piattaforme cloud con API REST e dashboard analytics.

### [INFO] Prerequisiti

- Python 3.11+
- Account su Heroku/Render/DigitalOcean
- Git

### 🏗️ Struttura Cloud

```
TokIntel_v2/
├── api/server.py          # FastAPI server
├── ui/analytics.py        # Dashboard Streamlit locale
├── ui/cloud_interface.py  # Interfaccia cloud
├── analytics/dashboard.py # Database analytics
├── integrations/telegram_bot.py # Notifiche Telegram
├── Dockerfile            # Container Docker
├── Procfile             # Config Heroku
└── requirements_cloud.txt # Dipendenze cloud
```

### 🌐 Deploy API FastAPI

#### Opzione 1: Heroku

```bash
# Clona il repository
git clone <your-repo>
cd TokIntel_v2

# Crea app Heroku
heroku create your-tokintel-app

# Configura variabili ambiente
heroku config:set TELEGRAM_API_KEY="your_key"
heroku config:set CHAT_ID="your_chat_id"

# Deploy
git add .
git commit -m "Deploy TokIntel v2.1"
git push heroku main
```

#### Opzione 2: Render

1. Vai su [Render.com](https://render.com)
2. Crea nuovo "Web Service"
3. Connetti il repository Git
4. Configura:
   - **Build Command**: `pip install -r requirements_cloud.txt`
   - **Start Command**: `uvicorn api.server:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: `TELEGRAM_API_KEY`, `CHAT_ID`

#### Opzione 3: Docker

```bash
# Build immagine
docker build -t tokintel-v2 .

# Esegui container
docker run -p 8000:8000 -p 8501:8501 tokintel-v2
```

### [REPORT] Dashboard Analytics

#### Locale (Streamlit)

```bash
# Installa dipendenze
pip install -r requirements_cloud.txt

# Avvia dashboard
streamlit run ui/analytics.py
```

#### Cloud (Streamlit Cloud)

1. Vai su [Streamlit Cloud](https://streamlit.io/cloud)
2. Connetti repository Git
3. Configura file: `ui/cloud_interface.py`
4. Imposta variabile ambiente: `API_BASE_URL`

### [INFO] Configurazione

#### File config.yaml

```yaml
# Configurazione base
model: "gpt-4"
language: "it"

# Telegram Bot (opzionale)
TELEGRAM_API_KEY: "your_bot_token"
CHAT_ID: "your_chat_id"

# API Settings
API_HOST: "0.0.0.0"
API_PORT: 8000
```

#### Variabili Ambiente

```bash
# Obbligatorie
TELEGRAM_API_KEY=your_bot_token
CHAT_ID=your_chat_id

# Opzionali
API_BASE_URL=https://your-api.herokuapp.com
```

### [INFO] Endpoint API

#### Analisi Video
```bash
POST /analyze/video
Content-Type: multipart/form-data
Body: file (video file)
```

#### Analisi Testo
```bash
POST /analyze/text
Content-Type: application/json
Body: {"content": "testo da analizzare", "title": "Titolo"}
```

#### Analytics
```bash
GET /analytics/top-videos?limit=10
GET /analytics/sentiment-trend
GET /analytics/keywords
```

### [INFO] Monitoraggio

#### Health Check
```bash
GET /health
Response: {"status": "healthy", "version": "2.1.0"}
```

#### Logs
```bash
# Heroku
heroku logs --tail

# Render
# Vai su dashboard > Logs

# Docker
docker logs <container_id>
```

### 🚨 Troubleshooting

#### Errore: "Module not found"
```bash
# Verifica requirements
pip install -r requirements_cloud.txt

# Controlla Python version
python --version  # Deve essere 3.11+
```

#### Errore: "Database locked"
```bash
# Riavvia il servizio
heroku restart

# Verifica connessioni SQLite
# Il problema è risolto automaticamente
```

#### Errore: "Telegram API"
```bash
# Verifica configurazione
echo $TELEGRAM_API_KEY
echo $CHAT_ID

# Test manuale
curl -X POST "https://api.telegram.org/bot$TELEGRAM_API_KEY/getMe"
```

### [REPORT] Scaling

#### Heroku
```bash
# Upgrade dyno
heroku ps:scale web=1:standard-1x

# Monitora performance
heroku addons:open scout
```

#### Render
- Auto-scaling disponibile
- Configura "Auto-Deploy" per aggiornamenti automatici

### [INFO] Sicurezza

#### CORS
```python
# Configurato automaticamente per tutti gli origin
# Modifica in api/server.py se necessario
```

#### Rate Limiting
```python
# Aggiungi middleware in api/server.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
```

### [INFO] Supporto

- **Issues**: GitHub Issues
- **Documentazione**: README.md
- **API Docs**: `/docs` (Swagger UI)

---

**TokIntel v2.1 Enterprise** - Deploy Cloud Ready! [INFO] 