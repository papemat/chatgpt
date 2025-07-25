# TokIntel v2 - Integrazione TikTok

## Panoramica

TokIntel v2 ora supporta l'importazione diretta di video TikTok tramite:
- **Login OAuth2** con TikTok
- **Scraping automatico** dei video salvati e collezioni
- **Importazione manuale** di link video

## [INFO] Funzionalità

### 1. Login con TikTok OAuth2
- Autenticazione sicura tramite API ufficiale TikTok
- Gestione automatica di access token e refresh token
- Fallback per cambiamenti API TikTok
- Persistenza sessione per riutilizzo

### 2. Scraping Video Salvati
- Estrazione automatica dei video salvati dall'account
- Supporto per collezioni personali
- Browser headless con Playwright
- Gestione sessioni browser per login persistente

### 3. Importazione Manuale
- Incolla link video direttamente
- Validazione automatica URL TikTok
- Supporto per batch di link

## [INFO] Prerequisiti

### 1. Credenziali TikTok Developer
1. Vai su [TikTok for Developers](https://developers.tiktok.com/)
2. Crea una nuova app
3. Configura le credenziali OAuth2
4. Imposta redirect URI: `http://localhost:8501/auth/callback`

### 2. Dipendenze
```bash
pip install playwright cryptography
playwright install chromium
```

## ⚙️ Configurazione

### 1. File di Configurazione
Modifica `config/config.yaml`:

```yaml
# TikTok OAuth Configuration
tiktok:
  client_key: "your_client_key_here"
  client_secret: "your_client_secret_here"
  redirect_uri: "http://localhost:8501/auth/callback"
  scope: "user.info.basic,video.list"
```

### 2. Configurazione via UI
1. Avvia l'interfaccia TikTok Import
2. Vai alla sezione "Configurazione OAuth"
3. Inserisci le credenziali
4. Salva la configurazione

## 🎯 Utilizzo

### 1. Avvio Interfaccia TikTok
```bash
# Dalla directory principale
python -m ui.import_tiktok

# Oppure tramite Streamlit
streamlit run ui/import_tiktok.py
```

### 2. Flusso di Login

#### Opzione A: Login Automatico
1. Configura le credenziali OAuth
2. Clicca "Login con Browser"
3. Completa l'autorizzazione TikTok
4. La sessione viene salvata automaticamente

#### Opzione B: Login Manuale
1. Clicca "Login Manuale"
2. Apri il browser e vai su TikTok
3. Fai login con le tue credenziali
4. Torna all'interfaccia TokIntel

### 3. Importazione Video

#### Video Salvati
1. Clicca "Importa Video Salvati"
2. Il sistema estrae automaticamente i video
3. Visualizza i risultati nell'interfaccia

#### Collezioni
1. Clicca "Importa Collezioni"
2. Seleziona le collezioni da importare
3. Importa i video dalle collezioni

#### Link Manuali
1. Incolla i link TikTok nell'area testo
2. Clicca "Importa Link"
3. I video vengono validati e importati

## [INFO] Architettura

### Moduli Principali

#### `auth/tiktok_oauth.py`
- Gestione OAuth2 TikTok
- Scambio token e refresh
- Fallback API endpoints
- Persistenza sessione

#### `scraper/tiktok_saves.py`
- Scraping browser headless
- Estrazione video salvati
- Gestione collezioni
- Session management

#### `ui/import_tiktok.py`
- Interfaccia Streamlit
- Gestione login
- Importazione video
- Visualizzazione risultati

### Flusso Dati
```
TikTok OAuth → Access Token → Browser Session → Scraping → Video Links → Analysis
```

## 🛡️ Sicurezza

### OAuth2 Security
- PKCE (Proof Key for Code Exchange)
- State parameter per CSRF protection
- Secure token storage
- Automatic token refresh

### Session Management
- Cookies encryption
- LocalStorage backup
- Session expiration (24h)
- Secure cleanup

### Privacy
- Nessun dato salvato permanentemente
- Session data locale only
- Configurable data retention

## [INFO] Fallback e Resilienza

### API Fallback
Il sistema include endpoint alternativi per:
- Autenticazione OAuth
- Token exchange
- User info retrieval

### Error Handling
- Retry automatico con backoff
- Graceful degradation
- User-friendly error messages
- Logging dettagliato

## [REPORT] Monitoraggio

### Logs
```bash
# Log di autenticazione
tail -f logs/tiktok_auth.log

# Log di scraping
tail -f logs/tiktok_scraper.log
```

### Metriche
- Video importati per sessione
- Success rate importazione
- Tempo di processing
- Errori e fallback usage

## 🚨 Troubleshooting

### Problemi Comuni

#### 1. "Client Key non configurato"
**Soluzione**: Configura le credenziali OAuth nel file config.yaml

#### 2. "Login fallito"
**Soluzione**: 
- Verifica credenziali TikTok
- Controlla redirect URI
- Prova login manuale

#### 3. "Nessun video trovato"
**Soluzione**:
- Verifica di avere video salvati
- Controlla privacy settings TikTok
- Prova con collezioni diverse

#### 4. "Browser non si avvia"
**Soluzione**:
```bash
playwright install chromium
playwright install-deps
```

### Debug Mode
```python
# Abilita debug logging
import logging
logging.getLogger('auth.tiktok_oauth').setLevel(logging.DEBUG)
logging.getLogger('scraper.tiktok_saves').setLevel(logging.DEBUG)
```

## [INFO] Roadmap

### Prossime Funzionalità
- [ ] Supporto per video pubblicati
- [ ] Analisi trend hashtag
- [ ] Export dati TikTok
- [ ] Integrazione con altri social
- [ ] Batch processing avanzato

### Miglioramenti
- [ ] Cache intelligente
- [ ] Rate limiting automatico
- [ ] Multi-account support
- [ ] API TikTok v3 support

## [INFO] Supporto

### Documentazione
- [README principale](../README.md)
- [Configurazione](../INSTALLATION_GUIDE.md)
- [API Reference](../docs/API.md)

### Issues
- GitHub Issues: [TokIntel Issues](https://github.com/your-repo/issues)
- Discord: [TokIntel Community](https://discord.gg/tokintel)

### Contributi
1. Fork il repository
2. Crea feature branch
3. Implementa le modifiche
4. Aggiungi test
5. Submit pull request

---

**Nota**: Questa integrazione rispetta i Terms of Service di TikTok. Utilizza solo le API ufficiali e i dati pubblicamente accessibili. 