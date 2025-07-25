# [INFO] Quick Start - TokIntel v2 Debug Tools

## ⚡ Utilizzo Rapido

### 1. **Audit Completo del Codice**
```bash
cd TokIntel_v2
python tools/debug_tools/audit_script.py
```

### 2. **Applicare Correzioni Automatiche**
```bash
python tools/debug_tools/fixes.py
```

### 3. **Verificare Risultati**
```bash
# Controllare i report generati
cat audit_report.json
cat fixes_report.json
```

---

## [INFO] Cosa Fa Ogni Tool

### [INFO] `audit_script.py`
- [OK] Scansiona tutti i file Python
- [OK] Identifica warning e errori
- [OK] Controlla deprecazioni asyncio
- [OK] Verifica problemi di sicurezza
- [OK] Genera report dettagliato

### [INFO] `fixes.py`
- [OK] Corregge deprecazioni asyncio
- [OK] Sostituisce `except:` con `except Exception:`
- [OK] Converte `print()` in `logger.info()`
- [OK] Rimuove import inutilizzati
- [OK] Aggiunge type hints mancanti

### ⚙️ `config.py`
- [OK] Configurazione centralizzata
- [OK] Pattern personalizzabili
- [OK] Impostazioni tool
- [OK] Opzioni report

---

## 🎯 Problemi Risolti

| Problema | Gravità | Soluzione |
|----------|---------|-----------|
| `asyncio.get_event_loop()` | [ERROR] Critico | Sostituito con `asyncio.get_running_loop()` |
| `except:` | [WARN] Medio | Sostituito con `except Exception:` |
| `print()` | [OK] Basso | Convertito in `logger.info()` |
| Import inutilizzati | [OK] Basso | Rimossi automaticamente |
| Type hints mancanti | [WARN] Medio | Aggiunti automaticamente |

---

## [REPORT] Output Esempio

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
  - Deprecated asyncio.get_event_loop() in main.py
  - Bare except clause in pipeline.py
  - Print statements in utils.py

FIXES APPLIED:
  - Fixed asyncio deprecations
  - Applied Black formatting
  - Removed unused imports
==================================================
```

---

## [INFO] Personalizzazione

### Modificare Pattern di Controllo
```python
# In config.py
WARNING_PATTERNS = [
    # Aggiungi i tuoi pattern
    (r'your_pattern', "Your warning message"),
]
```

### Disabilitare Tool
```python
# In config.py
TOOLS = {
    'black': {'enabled': False},
    'flake8': {'enabled': True},
}
```

### Cambiare Impostazioni Report
```python
# In config.py
REPORT_SETTINGS = {
    'max_warnings_display': 20,
    'save_report': True,
    'report_format': 'txt',
}
```

---

## 🚨 Codici di Uscita

- **0**: [OK] Nessun problema trovato
- **1**: [ERROR] Errori critici trovati
- **2**: [WARN]️ Solo warning trovati

---

## [INFO] Supporto Rapido

**Problema**: Tool non trovati
```bash
pip install black flake8 mypy autoflake
```

**Problema**: Percorso non corretto
```bash
# Assicurati di essere nella directory TokIntel_v2
pwd  # Dovrebbe mostrare .../TokIntel_v2
```

**Problema**: Permessi negati
```bash
# Su Windows
python tools/debug_tools/audit_script.py

# Su Linux/Mac
chmod +x tools/debug_tools/audit_script.py
./tools/debug_tools/audit_script.py
```

---

## 🎯 Prossimi Passi

1. **Eseguire audit completo**
2. **Applicare correzioni automatiche**
3. **Verificare risultati**
4. **Integrare in CI/CD**
5. **Configurare monitoraggio continuo**

---

**[INFO] Pronto per iniziare!**  
**[INFO] Per dettagli completi, vedi `README.md`** 