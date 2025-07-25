# 🧹 TokIntel v2.2 – Cleanup Plan Finale

_Audit e refactor trasversale su moduli critici_

---

## 🚦 Priorità Cleanup (Macro-task)

1. **Refactor e modularizzazione**
   - Suddividere classi manager troppo grandi (`DatabaseManager`, `TikTokIntegration`, ecc.)
   - Modularizzare funzioni lunghe in tutti i moduli (soprattutto `ui/`, `scraper/`, `batch_auto_analyze.py`)
   - Estrarre componenti UI riutilizzabili in `ui/components.py`

2. **Uniformare typing e docstring**
   - Aggiungere typing esplicito a tutti i metodi pubblici
   - Arricchire docstring per tutte le funzioni principali
   - Uniformare stile docstring (Google/NumPy)

3. **Logging e gestione errori**
   - Sostituire tutti i `print()` con logger strutturato
   - Logging dettagliato negli errori (incluso stacktrace)
   - Rendere i blocchi try/except più granulari e specifici

4. **Test e copertura**
   - Aggiungere test unitari/integrati per:
     - `DatabaseManager` e manager derivati
     - Funzioni di scraping e download
     - BatchAutoAnalyzer e CLI
     - Componenti UI critici (mock Streamlit)
   - Testare edge case (Playwright, scraping, errori di rete, DB)

5. **Pulizia e struttura progetto**
   - Rimuovere file/cartelle temporanee, duplicati, non usati (`__pycache__`, `.log`, `.tmp`, `.old`, `.zip`, ecc.)
   - Aggiornare `.gitignore` per ignorare file generati e temporanei
   - Verificare che non ci siano script legacy o non collegati

6. **Sicurezza e configurazione**
   - Verificare che nessuna credenziale sia hardcoded
   - Validare input utente e argomenti CLI
   - Migliorare gestione configurazioni (YAML centralizzato)

---

## [INFO] Checklist operativa

- [ ] Refactor classi manager troppo grandi
- [ ] Modularizzazione funzioni lunghe
- [ ] Estrarre componenti UI comuni
- [ ] Uniformare typing e docstring
- [ ] Logging strutturato ovunque
- [ ] Try/except granulari e logging errori
- [ ] Test unitari/integrati per moduli critici
- [ ] Test edge case scraping/DB
- [ ] Pulizia file/cartelle temporanei
- [ ] Aggiornamento `.gitignore`
- [ ] Rimozione script legacy/non usati
- [ ] Validazione input/config/CLI
- [ ] Nessuna credenziale hardcoded

---

## [INFO] Suggerimenti trasversali

- Centralizzare componenti UI e funzioni comuni
- Usare logger strutturato e livelli appropriati (info, warning, error)
- Documentare tutte le funzioni pubbliche
- Automatizzare i test e la formattazione (CI/CD)
- Aggiornare la documentazione dopo ogni refactor

---

**Pronto per la fase di refactor e cleanup!** 