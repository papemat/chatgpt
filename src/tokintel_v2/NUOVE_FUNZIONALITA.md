# [INFO] Nuove Funzionalità - TokIntel v2

Questo documento descrive le tre nuove funzionalità implementate secondo le specifiche richieste.

## [INFO] Indice

1. [Gestione Status Video](#gestione-status-video)
2. [Analisi Trend Personali](#analisi-trend-personali)
3. [Auto-Analisi Batch](#auto-analisi-batch)
4. [Configurazione](#configurazione)
5. [Utilizzo](#utilizzo)

---

## [OK] 1. Gestione Status Video

### Descrizione
Sistema per distinguere facilmente i video:
- [WARN] **Nuovi** (mai analizzati)
- [OK] **Analizzati** (con risultati salvati)
- [ERROR] **Errore** (analisi fallita o incompleta)

### Implementazione

#### Database
- **Tabella**: `user_saved_videos`
- **Nuovo campo**: `status` (Enum: 'new', 'analyzed', 'error')
- **Default**: 'new'

#### Funzioni Aggiunte
```python
# Aggiorna status di un video
db_manager.update_video_status(video_id, status)

# Recupera video per status
db_manager.get_videos_by_status(user_id, status)
```

#### Interfaccia
- **Filtro status** nella sidebar di `tiktok_library.py`
- **Badge colorati** per ogni video
- **Statistiche rapide** nella sidebar

### Utilizzo
1. Apri "My TikTok Library"
2. Usa il filtro "Stato Analisi" nella sidebar
3. I video mostrano badge colorati per lo status
4. Le statistiche mostrano conteggi per ogni status

---

## [REPORT] 2. Analisi Trend Personali

### Descrizione
Visualizzazione dei pattern nei contenuti TikTok dell'utente:
- **Parole chiave** più utilizzate
- **Emozioni** più frequenti
- **Trend temporali** delle performance
- **Temi del contenuto** identificati

### Implementazione

#### Modulo: `analytics/trend_analyzer.py`
```python
class TrendAnalyzer:
    def aggregate_keywords(user_id, days=30)
    def aggregate_emotions(user_id, days=30)
    def trend_over_time(user_id, days=90)
    def get_user_insights(user_id, days=30)
    def get_content_themes(user_id, days=30)
```

#### Interfaccia: `ui/trend_personale.py`
- **Dashboard dedicata** per i trend personali
- **Grafici interattivi** (Plotly)
- **Filtri temporali** (7, 30, 90, 180, 365 giorni)
- **Esportazione dati** (JSON, CSV)

### Funzionalità

#### [REPORT] Grafici Disponibili
1. **Bar Chart** - Top 20 parole chiave
2. **Pie Chart** - Distribuzione emozioni
3. **Line Chart** - Trend performance nel tempo
4. **Temi del contenuto** - Categorizzazione automatica

#### 🎯 Emozioni Identificate
- Felicità, Tristezza, Rabbia, Paura
- Sorpresa, Disgusto, Amore
- Motivazione, Umorismo, Calma

#### [REPORT] Insights Generati
- Video analizzati nel periodo
- Keyword più utilizzata
- Emozione più frequente
- Percentuale di completamento analisi

### Utilizzo
1. Apri "Trend Personale" dal menu
2. Seleziona periodo di analisi
3. Esplora i grafici e insights
4. Esporta i dati se necessario

---

## [INFO] 3. Auto-Analisi Batch

### Descrizione
Sistema per analizzare automaticamente tutti i video non ancora analizzati:
- **Rilevamento automatico** dei video nuovi
- **Analisi sequenziale** con progress tracking
- **Gestione errori** e retry
- **Notifiche di completamento**

### Implementazione

#### Modulo: `batch_auto_analyze.py`
```python
class BatchAutoAnalyzer:
    def get_pending_videos(user_id)
    async def analyze_single_video(video_data)
    async def analyze_pending_videos(user_id, progress_callback)
    def get_analysis_summary(user_id)
```

#### Funzionalità CLI
```bash
# Analizza tutti i video pending
python batch_auto_analyze.py --user-id 1

# Mostra solo riepilogo
python batch_auto_analyze.py --user-id 1 --summary

# Salva risultati in file
python batch_auto_analyze.py --user-id 1 --output results.json
```

#### Integrazione UI
- **Bottone "Analizza Tutti i Nuovi Video"** nella sidebar
- **Progress bar** con aggiornamenti in tempo reale
- **Statistiche status** nella sidebar
- **Notifiche di completamento**

### Configurazione
```yaml
batch_analysis:
  max_concurrent: 3        # Analisi simultanee
  delay_seconds: 2         # Delay tra analisi
  retry_attempts: 2        # Tentativi per errore
  auto_analyze_on_save: false
```

### Utilizzo
1. Apri "My TikTok Library"
2. Controlla le statistiche nella sidebar
3. Clicca "[INFO] Analizza Tutti i Nuovi Video"
4. Monitora il progresso
5. Visualizza i risultati

---

## ⚙️ 4. Configurazione

### File: `config.yaml`

#### Batch Analysis
```yaml
batch_analysis:
  max_concurrent: 3
  delay_seconds: 2
  retry_attempts: 2
  auto_analyze_on_save: false
```

#### Trend Analysis
```yaml
trend_analysis:
  default_period_days: 30
  max_keywords: 20
  max_emotions: 10
  min_frequency: 1
```

#### Video Status
```yaml
video_status:
  auto_update_on_analysis: true
  default_status: "new"
  status_options: ["new", "analyzed", "error"]
```

---

## [INFO] 5. Utilizzo

### Avvio delle Funzionalità

#### 1. Libreria con Status
```bash
cd TokIntel_v2
streamlit run ui/tiktok_library.py
```

#### 2. Trend Personali
```bash
cd TokIntel_v2
streamlit run ui/trend_personale.py
```

#### 3. Auto-Analisi Batch
```bash
cd TokIntel_v2
python batch_auto_analyze.py --user-id 1
```

### Workflow Tipico

1. **Importa video** tramite `import_tiktok.py`
2. **Visualizza status** in `tiktok_library.py`
3. **Analizza batch** dei video nuovi
4. **Esplora trend** in `trend_personale.py`
5. **Esporta insights** per analisi esterne

### Integrazione con Sistema Esistente

Le nuove funzionalità si integrano perfettamente con:
- [OK] Sistema di database esistente
- [OK] Interfacce Streamlit esistenti
- [OK] Sistema di logging
- [OK] Configurazione centralizzata
- [OK] Gestione errori

---

## [INFO] Troubleshooting

### Problemi Comuni

#### 1. Status non aggiornato
```bash
# Verifica database
python -c "from db.database import get_db_manager; print(get_db_manager().get_videos_by_status(1, 'new'))"
```

#### 2. Trend non visualizzati
```bash
# Verifica analisi esistenti
python -c "from analytics.trend_analyzer import get_trend_analyzer; print(get_trend_analyzer().get_user_insights(1))"
```

#### 3. Auto-analisi non funziona
```bash
# Test manuale
python batch_auto_analyze.py --user-id 1 --summary
```

### Log Files
- **Database**: `logs/database.log`
- **Analisi**: `logs/analysis.log`
- **Batch**: `logs/batch_analysis.log`

---

## [REPORT] Metriche e Performance

### Performance Attese
- **Analisi singola**: 30-60 secondi
- **Batch 10 video**: 5-10 minuti
- **Trend analysis**: 1-3 secondi
- **UI loading**: < 2 secondi

### Scalabilità
- **Video per utente**: 1000+
- **Analisi simultanee**: 3 (configurabile)
- **Periodo trend**: fino a 1 anno
- **Storage**: dipende da video

---

## 🎯 Prossimi Sviluppi

### Funzionalità Future
1. **Notifiche Telegram** per completamento batch
2. **Cron job** per auto-analisi notturna
3. **Machine Learning** per predizione trend
4. **API REST** per integrazione esterna
5. **Dashboard avanzate** con più metriche

### Ottimizzazioni
1. **Analisi parallela** per video multipli
2. **Cache intelligente** per trend
3. **Compressione video** automatica
4. **Backup automatico** database

---

## [INFO] Supporto

Per problemi o domande:
1. Controlla i log in `logs/`
2. Verifica la configurazione in `config.yaml`
3. Testa le funzionalità individualmente
4. Consulta la documentazione esistente

---

*Documento aggiornato: 2024-12-19*
*Versione: TokIntel v2.1* 