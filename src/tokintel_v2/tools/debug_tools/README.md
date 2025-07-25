# TokIntel v2 - Debug Tools

Tool automatici per audit, debug e rimozione warning del codice TokIntel v2.

## [INFO] Funzionalità

- **Audit automatico** del codice Python
- **Rimozione import inutilizzati** con autoflake
- **Formattazione automatica** con Black
- **Controlli di stile** con Flake8
- **Type checking** con MyPy
- **Controlli di sicurezza** per credenziali hardcoded
- **Controlli async/await** per problemi di concorrenza
- **Report dettagliati** in formato JSON

## [INFO] Prerequisiti

Installa i tool necessari:

```bash
pip install black flake8 mypy autoflake
```

## [INFO] Utilizzo

### Audit Completo

```bash
cd TokIntel_v2/tools/debug_tools
python audit_script.py
```

### Audit Specifico

```python
from audit_script import TokIntelAuditor

# Audit di un file specifico
auditor = TokIntelAuditor("path/to/project")
report = auditor.run_full_audit()
auditor.print_summary()
```

## [REPORT] Report

Il tool genera un report dettagliato in `audit_report.json` con:

- **Warnings trovati**: Problemi di stile, import inutilizzati, ecc.
- **Errori critici**: Problemi che impediscono l'esecuzione
- **Fix applicati**: Correzioni automatiche effettuate
- **Problemi di sicurezza**: Credenziali hardcoded, vulnerabilità
- **Problemi di performance**: Codice inefficiente

## ⚙️ Configurazione

Modifica `config.py` per personalizzare:

- **Tool abilitati**: Black, Flake8, MyPy, Autoflake
- **Pattern di controllo**: Warning, sicurezza, performance
- **Directory escluse**: __pycache__, .git, venv, ecc.
- **Impostazioni report**: Formato, dettagli, ecc.

## [INFO] Tipi di Controlli

### 1. Import Inutilizzati
- Rimozione automatica con autoflake
- Import wildcard (`import *`)
- Import multipli sulla stessa riga

### 2. Stile del Codice
- Formattazione Black
- Linting Flake8
- Lunghezza righe
- Spaziature

### 3. Type Checking
- Controlli MyPy
- Annotazioni di tipo
- Import mancanti

### 4. Problemi Async
- `await` fuori da funzioni async
- `asyncio.get_event_loop()` deprecato
- `asyncio.run()` annidati

### 5. Sicurezza
- Credenziali hardcoded
- `eval()`, `exec()`, `input()`
- `os.system()` e `subprocess.call()`

### 6. Performance
- Loop inefficienti
- List comprehension vs append
- Funzioni vuote

## [INFO] Esempi di Output

```
==================================================
TOKINTEL V2 AUDIT SUMMARY
==================================================
Python files audited: 15
Warnings found: 8
Errors found: 0
Fixes applied: 3
Style issues: 2
Security issues: 1

WARNINGS:
  - Wildcard imports detected in main.py
  - Bare except clauses detected in pipeline.py
  - Print statements detected in utils.py

FIXES APPLIED:
  - Removed unused imports from main.py
  - Applied Black formatting
  - Fixed line length issues
==================================================
```

## 🚨 Codici di Uscita

- **0**: Nessun problema trovato
- **1**: Errori critici trovati
- **2**: Solo warning trovati

## [INFO] Personalizzazione

### Aggiungere Nuovi Pattern

```python
# In config.py
WARNING_PATTERNS = [
    # ... pattern esistenti ...
    (r'your_pattern', "Your warning message"),
]
```

### Disabilitare Tool

```python
# In config.py
TOOLS = {
    'black': {'enabled': False},
    'flake8': {'enabled': True},
    # ...
}
```

### Modificare Impostazioni Report

```python
# In config.py
REPORT_SETTINGS = {
    'max_warnings_display': 20,
    'save_report': True,
    'report_format': 'txt',
}
```

## 🤝 Contribuire

1. Aggiungi nuovi pattern di controllo
2. Migliora la configurazione
3. Aggiungi nuovi tool di audit
4. Migliora la documentazione

## [INFO] Supporto

Per problemi o suggerimenti:
- Apri una issue su GitHub
- Contatta il team di sviluppo
- Consulta la documentazione principale di TokIntel v2 