# [INFO] Guida alla Libreria TikTok - TokIntel v2

## Panoramica

Questa guida descrive le nuove funzionalità implementate per la gestione automatica dei video TikTok salvati, incluse:

- **Download automatico dei video TikTok**
- **Dashboard "My TikTok Library"**
- **Integrazione con database PostgreSQL**
- **Sincronizzazione automatica delle librerie**

## [INFO] 1. Download Automatico Video TikTok

### Modulo: `scraper/download_tiktok_video.py`

Il modulo `TikTokVideoDownloader` gestisce il download automatico dei video TikTok con cache locale.

#### Caratteristiche principali:

- **Cache locale**: I video vengono salvati in `cache/videos/`
- **Gestione metadati**: Ogni video ha un file JSON associato con metadati
- **Controllo duplicati**: Evita download multipli dello stesso video
- **Gestione errori**: Gestione robusta degli errori di download

#### Utilizzo base:

```python
from scraper.download_tiktok_video import TikTokVideoDownloader

async with TikTokVideoDownloader() as downloader:
    result = await downloader.download_video_with_metadata(
        "https://www.tiktok.com/@username/video/1234567890123456789",
        metadata={'user_id': 1, 'analysis_ready': True}
    )
    print(f"Download completato: {result}")
```

#### Funzioni di utilità:

```python
# Download per analisi
from scraper.download_tiktok_video import download_video_for_analysis

result = await download_video_for_analysis(
    "https://www.tiktok.com/@username/video/1234567890123456789",
    user_id=1
)

# Ottieni video in cache per utente
from scraper.download_tiktok_video import get_user_cached_videos

videos = await get_user_cached_videos(user_id=1)
```

## [INFO] 2. Dashboard "My TikTok Library"

### Modulo: `ui/tiktok_library.py`

Dashboard Streamlit completa per la gestione della libreria TikTok.

#### Funzionalità:

- **Visualizzazione video**: Griglia con anteprima e metadati
- **Filtri avanzati**: Per data, stato, punteggio, dimensione
- **Analytics**: Grafici e statistiche della libreria
- **Esportazione**: JSON, CSV, PDF
- **Cronologia analisi**: Storico delle analisi effettuate

#### Avvio della dashboard:

```bash
cd TokIntel_v2
streamlit run ui/tiktok_library.py
```

#### Sezioni principali:

1. **[INFO] Libreria**: Visualizzazione e gestione video
2. **[REPORT] Analytics**: Statistiche e grafici
3. **[INFO] Esportazione**: Esportazione dati e video
4. **[INFO] Cronologia**: Storico analisi

#### Filtri disponibili:

- **Periodo**: Ultimi 7/30 giorni, 3 mesi, anno
- **Stato**: Analizzato, In attesa, Errore
- **Punteggio**: Range personalizzabile
- **Ordinamento**: Data, punteggio, dimensione, nome

## [INFO] 3. Integrazione Database PostgreSQL

### Nuove tabelle aggiunte:

#### `user_tiktok_sessions`
Gestisce le sessioni TikTok degli utenti:

```sql
CREATE TABLE user_tiktok_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tiktok_username VARCHAR(100) NOT NULL,
    session_data JSON,
    is_active BOOLEAN DEFAULT TRUE,
    login_method VARCHAR(50),
    last_activity TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### `user_saved_videos`
Gestisce i video TikTok salvati:

```sql
CREATE TABLE user_saved_videos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id INTEGER REFERENCES user_tiktok_sessions(id),
    tiktok_video_id VARCHAR(100) NOT NULL,
    video_url VARCHAR(500) NOT NULL,
    video_title VARCHAR(200),
    creator_username VARCHAR(100),
    duration VARCHAR(50),
    resolution VARCHAR(50),
    view_count INTEGER,
    like_count INTEGER,
    comment_count INTEGER,
    share_count INTEGER,
    local_file_path VARCHAR(500),
    file_size_mb FLOAT,
    download_status VARCHAR(50) DEFAULT 'pending',
    analysis_id INTEGER REFERENCES video_analyses(id),
    saved_at TIMESTAMP DEFAULT NOW(),
    downloaded_at TIMESTAMP,
    analyzed_at TIMESTAMP
);
```

### Metodi database aggiunti:

```python
from db.database import get_db_manager

db = get_db_manager()

# Gestione sessioni TikTok
session = db.create_tiktok_session(user_id, username, session_data)
active_session = db.get_active_tiktok_session(user_id)
db.update_tiktok_session_activity(session_id)
db.deactivate_tiktok_session(session_id)

# Gestione video salvati
video = db.save_tiktok_video(user_id, video_data)
db.update_video_download_status(video_id, 'downloaded', file_path, size)
db.link_video_to_analysis(video_id, analysis_id)
videos = db.get_user_saved_videos(user_id)
videos_with_analysis = db.get_videos_with_analysis(user_id)
```

## [INFO] 4. Modulo di Integrazione

### Modulo: `scraper/tiktok_integration.py`

Il modulo `TikTokIntegration` fornisce un'interfaccia unificata per tutte le operazioni TikTok.

#### Funzionalità principali:

- **Setup sessione**: Configurazione automatica sessioni TikTok
- **Sincronizzazione**: Sincronizzazione automatica video salvati
- **Download batch**: Download automatico di video non scaricati
- **Preparazione analisi**: Preparazione video per analisi
- **Riepilogo libreria**: Statistiche complete della libreria

#### Utilizzo:

```python
from scraper.tiktok_integration import TikTokIntegration

integration = TikTokIntegration()

# Setup sessione utente
session = await integration.setup_user_session(
    user_id=1,
    tiktok_username="my_username",
    session_data={"cookies": {...}, "tokens": {...}}
)

# Sincronizza video salvati
synced_videos = await integration.sync_saved_videos(user_id=1, max_videos=50)

# Scarica video non scaricati
downloaded_videos = await integration.download_user_videos(user_id=1, max_videos=10)

# Prepara video per analisi
video_id = await integration.process_video_for_analysis(user_id=1, video_id=123)

# Ottieni riepilogo libreria
summary = integration.get_user_library_summary(user_id=1)
```

#### Funzioni di utilità:

```python
from scraper.tiktok_integration import integrate_tiktok_user, sync_user_tiktok_library

# Integrazione completa utente
success = await integrate_tiktok_user(
    user_id=1,
    tiktok_username="my_username",
    session_data={"cookies": {...}}
)

# Sincronizzazione completa libreria
result = await sync_user_tiktok_library(user_id=1)
```

## [INFO] 5. Configurazione e Setup

### Prerequisiti:

1. **Playwright**: Installazione browser per scraping
```bash
pip install playwright
playwright install chromium
```

2. **Dipendenze aggiuntive**:
```bash
pip install aiohttp aiofiles
```

3. **Database**: PostgreSQL configurato con le nuove tabelle

### Configurazione cache:

La cache dei video viene salvata in `cache/videos/` con struttura:

```
cache/videos/
├── 1234567890123456789.mp4
├── 1234567890123456789_metadata.json
├── 9876543210987654321.mp4
└── 9876543210987654321_metadata.json
```

### Variabili d'ambiente:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tokintel
DB_USER=postgres
DB_PASSWORD=password

# Cache
TIKTOK_CACHE_DIR=cache/videos
```

## [INFO] 6. Flusso di Utilizzo Tipico

### 1. Setup iniziale utente:

```python
# Configura sessione TikTok
session = await integration.setup_user_session(
    user_id=1,
    tiktok_username="my_username",
    session_data=session_data
)

# Sincronizza video salvati
synced = await integration.sync_saved_videos(user_id=1)
```

### 2. Download automatico:

```python
# Scarica video non scaricati
downloaded = await integration.download_user_videos(user_id=1)
```

### 3. Utilizzo dashboard:

```bash
# Avvia dashboard
streamlit run ui/tiktok_library.py
```

### 4. Analisi video:

```python
# Prepara video per analisi
video_id = await integration.process_video_for_analysis(user_id=1, video_id=123)

# Il video è ora pronto per l'analisi con il sistema esistente
```

## [INFO] 7. Gestione Errori

### Errori comuni e soluzioni:

1. **Playwright non installato**:
```bash
pip install playwright
playwright install chromium
```

2. **Sessione TikTok scaduta**:
```python
# Ricrea sessione
session = await integration.setup_user_session(user_id, username, new_session_data)
```

3. **Video non scaricabile**:
```python
# Verifica stato
video = db.get_video_by_tiktok_id(user_id, video_id)
if video.download_status == 'failed':
    # Riprova download
    await integration.process_video_for_analysis(user_id, video.id)
```

4. **Database non accessibile**:
```python
# Verifica connessione
db = get_db_manager()
with db.get_session() as session:
    # Test query
    pass
```

## [INFO] 8. Monitoraggio e Logging

### Log principali:

- **Download**: `scraper.download_tiktok_video`
- **Integrazione**: `scraper.tiktok_integration`
- **Database**: `db.database`
- **Dashboard**: `ui.tiktok_library`

### Metriche da monitorare:

- Numero video sincronizzati
- Tasso di successo download
- Dimensione cache
- Tempo di sincronizzazione
- Errori di sessione

## [INFO] 9. Estensioni Future

### Possibili miglioramenti:

1. **Scheduling automatico**: Sincronizzazione periodica
2. **Notifiche**: Alert per nuovi video
3. **Analisi batch**: Analisi automatica di video non analizzati
4. **Backup**: Backup automatico della cache
5. **API REST**: Endpoint per integrazione esterna

### Esempio scheduling:

```python
import asyncio
import schedule
import time

async def daily_sync():
    result = await sync_user_tiktok_library(user_id=1)
    print(f"Sync completata: {result}")

# Sincronizzazione giornaliera alle 6:00
schedule.every().day.at("06:00").do(lambda: asyncio.run(daily_sync()))

while True:
    schedule.run_pending()
    time.sleep(60)
```

## [INFO] 10. Supporto e Troubleshooting

### Contatti:

- **Documentazione**: Questo file
- **Issues**: Repository GitHub
- **Logs**: File di log in `logs/`

### Debug comune:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Test downloader
async with TikTokVideoDownloader(headless=False) as downloader:
    result = await downloader.download_video_with_metadata(test_url)
    print(f"Debug result: {result}")
```

---

**Nota**: Queste funzionalità sono integrate con il sistema TokIntel esistente e mantengono la compatibilità con tutte le funzionalità precedenti. 