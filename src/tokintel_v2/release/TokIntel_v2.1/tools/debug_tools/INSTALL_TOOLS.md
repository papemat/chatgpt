# [INFO] Installazione Tool Esterni - TokIntel v2

## [INFO] Tool Richiesti

Per un audit completo di TokIntel v2, installa i seguenti tool:

---

## [INFO] Installazione Rapida

### **Windows (PowerShell)**
```powershell
pip install black flake8 mypy autoflake
```

### **Linux/macOS (Terminal)**
```bash
pip install black flake8 mypy autoflake
```

### **Con Virtual Environment**
```bash
# Attiva il virtual environment
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate     # Windows

# Installa i tool
pip install black flake8 mypy autoflake
```

---

## [INFO] Dettagli Tool

### **Black** - Formattatore Codice
```bash
pip install black
```
- **Scopo**: Formattazione automatica del codice Python
- **Configurazione**: Usa configurazione in `config.py`
- **Utilizzo**: `black TokIntel_v2/`

### **Flake8** - Linter
```bash
pip install flake8
```
- **Scopo**: Controllo stile e qualità codice
- **Configurazione**: `.flake8` o parametri CLI
- **Utilizzo**: `flake8 TokIntel_v2/`

### **MyPy** - Type Checker
```bash
pip install mypy
```
- **Scopo**: Controllo tipi statici
- **Configurazione**: `mypy.ini` o parametri CLI
- **Utilizzo**: `mypy TokIntel_v2/`

### **Autoflake** - Rimozione Import
```bash
pip install autoflake
```
- **Scopo**: Rimozione automatica import inutilizzati
- **Configurazione**: Parametri CLI
- **Utilizzo**: `autoflake --remove-all-unused-imports file.py`

---

## ⚙️ Configurazione

### **Black Configuration**
Crea `pyproject.toml` nella root:
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### **Flake8 Configuration**
Crea `.flake8` nella root:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info
```

### **MyPy Configuration**
Crea `mypy.ini` nella root:
```ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy.plugins.numpy.*]
ignore_missing_imports = True
```

---

## [INFO] Test Installazione

### **Verifica Installazione**
```bash
# Verifica che tutti i tool siano installati
black --version
flake8 --version
mypy --version
autoflake --version
```

### **Test Rapido**
```bash
# Test Black
black --check TokIntel_v2/

# Test Flake8
flake8 TokIntel_v2/

# Test MyPy
mypy TokIntel_v2/

# Test Autoflake
autoflake --remove-all-unused-imports --check TokIntel_v2/main.py
```

---

## [INFO] Aggiornamento

### **Aggiorna Tutti i Tool**
```bash
pip install --upgrade black flake8 mypy autoflake
```

### **Aggiorna Singolo Tool**
```bash
pip install --upgrade black
pip install --upgrade flake8
pip install --upgrade mypy
pip install --upgrade autoflake
```

---

## 🚨 Risoluzione Problemi

### **Problema: Tool non trovato**
```bash
# Verifica PATH
echo $PATH  # Linux/macOS
$env:PATH   # Windows PowerShell

# Reinstalla
pip uninstall black flake8 mypy autoflake
pip install black flake8 mypy autoflake
```

### **Problema: Permessi negati**
```bash
# Usa --user flag
pip install --user black flake8 mypy autoflake

# Oppure usa sudo (Linux/macOS)
sudo pip install black flake8 mypy autoflake
```

### **Problema: Versioni conflittuali**
```bash
# Crea nuovo virtual environment
python -m venv venv_new
source venv_new/bin/activate  # Linux/macOS
venv_new\Scripts\activate     # Windows
pip install black flake8 mypy autoflake
```

---

## [REPORT] Dopo l'Installazione

### **Esegui Audit Completo**
```bash
cd TokIntel_v2
python tools/debug_tools/audit_script.py
```

### **Aspettati Risultati**
- [OK] Black: Formattazione automatica
- [OK] Flake8: Controlli stile
- [OK] MyPy: Type checking
- [OK] Autoflake: Rimozione import

### **Report Migliorato**
Con tutti i tool installati, l'audit fornirà:
- Controlli di stile completi
- Type checking dettagliato
- Rimozione automatica import
- Report più accurati

---

## 🎯 Prossimi Passi

1. **Installa i tool** con i comandi sopra
2. **Esegui audit completo** per verificare
3. **Configura CI/CD** per automazione
4. **Documenta processi** per il team

---

**[OK] Pronto per audit professionale!**  
**[INFO] Consulta `README.md` per dettagli completi** 