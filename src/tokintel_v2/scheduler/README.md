# ⏰ Auto-Analyze Scheduler - TokIntel v2

## [INFO] Panoramica

Il modulo `scheduler` implementa un sistema di **auto-analisi schedulata** per TokIntel v2, che esegue automaticamente l'analisi dei video TikTok salvati ma non ancora analizzati a intervalli regolari.

## [INFO] Funzionalità

- [OK] **Schedulazione automatica** con APScheduler
- [OK] **Esecuzione periodica** dell'analisi batch
- [OK] **Gestione errori** e logging dettagliato
- [OK] **CLI completa** per controllo da riga di comando
- [OK] **Integrazione** con il sistema esistente

## [INFO] Installazione

### 1. Dipendenze

Il modulo richiede `APScheduler`. È già incluso in `requirements.txt`:

```bash
pip install apscheduler>=3.10.0
```

### 2. Struttura

```
TokIntel_v2/
├── scheduler/
│   ├── __init__.py
│   ├── auto_scheduler.py
│   └── README.md
└── tests/
    └── test_auto_scheduler.py
```

## [INFO] Utilizzo

### CLI (Riga di Comando)

#### Avvio dello Scheduler

```bash
# Avvia scheduler per user_id=1 con intervallo di 60 minuti (default)
python scheduler/auto_scheduler.py --user-id 1

# Avvia scheduler con intervallo personalizzato (15 minuti)
python scheduler/auto_scheduler.py --user-id 1 --interval 15

# Avvia scheduler con intervallo di 6 ore
python scheduler/auto_scheduler.py --user-id 1 --interval 360
```

#### Controllo dello Scheduler

```bash
# Verifica status dello scheduler
python scheduler/auto_scheduler.py --user-id 1 --status

# Ferma lo scheduler
python scheduler/auto_scheduler.py --user-id 1 --stop
```

### Programmatico

#### Avvio Semplice

```python
from scheduler import start_auto_analyzer

# Avvia scheduler per user_id=1 ogni 60 minuti
success = start_auto_analyzer(user_id=1, interval_minutes=60)

if success:
    print("[OK] Scheduler avviato con successo")
else:
    print("[ERROR] Errore nell'avvio dello scheduler")
```

#### Controllo Avanzato

```python
from scheduler import (
    start_auto_analyzer,
    stop_auto_analyzer,
    get_auto_analyzer_status,
    get_scheduler
)

# Avvia scheduler
start_auto_analyzer(user_id=1, interval_minutes=30)

# Verifica status
status = get_auto_analyzer_status()
print(f"Status: {status}")

# Ferma scheduler
stop_auto_analyzer()
```

#### Utilizzo della Classe Diretta

```python
from scheduler import AutoAnalyzeScheduler

# Crea istanza
scheduler = AutoAnalyzeScheduler()

# Avvia
success = scheduler.start_auto_analyzer(user_id=1, interval_minutes=60)

# Verifica status
status = scheduler.get_status()
print(f"Scheduler attivo: {status['is_running']}")

# Ferma
scheduler.stop_scheduler()
```

## [REPORT] Output e Logging

### Messaggi di Log

Lo scheduler produce messaggi di log dettagliati:

```
[OK] [TokIntel Scheduler] Avviato per user_id=1 - intervallo: 60 min
[OK] [TokIntel Auto] Analisi avviata - 16:00
✔️ Completati 5 video - [ERROR] 0 errori
[OK] [TokIntel Auto] Analisi avviata - 17:00
✔️ Completati 2 video - [ERROR] 1 errore
[WARN]️ Errore video: Video ID 123 - Errore di analisi
```

### Risultati dell'Analisi

Ogni esecuzione restituisce:

```python
{
    'analyzed': 3,        # Video analizzati con successo
    'errors': 1,          # Video con errori
    'total_videos': 4,    # Totale video processati
    'duration': 45.2,     # Tempo di esecuzione in secondi
    'error_details': [...] # Dettagli errori (se presenti)
}
```

## ⚙️ Configurazione

### Intervalli Consigliati

| Scenario | Intervallo | Comando |
|----------|------------|---------|
| **Test/Dev** | 15 minuti | `--interval 15` |
| **Produzione** | 1 ora | `--interval 60` |
| **Server 24/7** | 6 ore | `--interval 360` |
| **Analisi intensiva** | 30 minuti | `--interval 30` |

### Integrazione con Streamlit

```python
import streamlit as st
from scheduler import start_auto_analyzer, get_auto_analyzer_status

# Sidebar per controllo scheduler
with st.sidebar:
    st.header("[INFO] Auto-Analyze Scheduler")
    
    if st.button("Avvia Scheduler"):
        success = start_auto_analyzer(user_id=1, interval_minutes=60)
        if success:
            st.success("Scheduler avviato!")
        else:
            st.error("Errore nell'avvio")
    
    # Mostra status
    status = get_auto_analyzer_status()
    st.json(status)
```

## [INFO] Testing

### Esecuzione Test

```bash
# Test unitari
pytest tests/test_auto_scheduler.py -v

# Test con coverage
pytest tests/test_auto_scheduler.py --cov=scheduler --cov-report=html
```

### Test Manuali

```bash
# Test avvio scheduler (1 minuto di intervallo)
python scheduler/auto_scheduler.py --user-id 999 --interval 1

# Premi Ctrl+C dopo alcuni minuti per fermare
```

## [INFO] Troubleshooting

### Problemi Comuni

#### 1. Errore Import APScheduler
```
ModuleNotFoundError: No module named 'apscheduler'
```
**Soluzione**: Installa APScheduler
```bash
pip install apscheduler>=3.10.0
```

#### 2. Scheduler Non Si Avvia
```
[ERROR] Errore nell'avvio dello scheduler
```
**Soluzione**: Verifica che:
- Il database sia accessibile
- I moduli core siano importabili
- Non ci siano altri scheduler attivi

#### 3. Job Non Eseguiti
**Soluzione**: Verifica i log per errori specifici e controlla che:
- I video abbiano `status = 'new'`
- I file video esistano localmente
- Il sistema di analisi sia funzionante

### Debug

Abilita logging dettagliato:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## [REPORT] Monitoraggio

### Metriche da Monitorare

- **Frequenza esecuzioni**: Verifica che i job vengano eseguiti regolarmente
- **Tempo di esecuzione**: Monitora la durata delle analisi
- **Tasso di successo**: Controlla il rapporto tra video analizzati e errori
- **Risorse sistema**: CPU, memoria, spazio disco

### Log di Sistema

I log vengono salvati tramite il sistema di logging di TokIntel:

```python
from core.logger import setup_logger
logger = setup_logger(__name__)
```

## [INFO] Integrazione con Altri Sistemi

### Cron Job (Linux/macOS)

```bash
# Esegui ogni 6 ore
0 */6 * * * cd /path/to/TokIntel_v2 && python scheduler/auto_scheduler.py --user-id 1 --interval 360
```

### Windows Task Scheduler

Crea un file `start_scheduler.bat`:

```batch
@echo off
cd /d "C:\path\to\TokIntel_v2"
python scheduler\auto_scheduler.py --user-id 1 --interval 60
```

### Docker

```dockerfile
# Aggiungi al Dockerfile
RUN pip install apscheduler>=3.10.0

# Comando di avvio
CMD ["python", "scheduler/auto_scheduler.py", "--user-id", "1", "--interval", "60"]
```

## [INFO] Note di Sviluppo

### Architettura

- **Singleton Pattern**: Una sola istanza dello scheduler per processo
- **Async Support**: Utilizza AsyncIOScheduler per compatibilità con asyncio
- **Error Handling**: Gestione robusta degli errori con logging
- **Resource Management**: Cleanup automatico delle risorse

### Estensioni Future

- [ ] Supporto per più utenti simultanei
- [ ] Configurazione tramite file YAML
- [ ] Notifiche Telegram/Email
- [ ] Dashboard web per monitoraggio
- [ ] Retry automatico per video falliti

---

**Autore**: TokIntel v2 Team  
**Versione**: 1.0.0  
**Data**: 2024 