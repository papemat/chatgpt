# Devika TokIntel - Enhanced AI Integration System

## [INFO] **Nuove Funzionalità: Gestione Automatica Modelli**

### ✨ **Caratteristiche Principali**

- **🤖 Gestione Automatica Modelli**: Download e configurazione automatica per LM Studio e Ollama
- **[INFO] Router Intelligente**: Selezione automatica del miglior backend LLM disponibile
- **[INFO] Verifica Modelli**: Controllo automatico della disponibilità dei modelli
- **[INFO] Istruzioni Automatiche**: Guide dettagliate per il download manuale quando necessario
- **⚡ Benchmark Avanzato**: Confronto completo delle performance tra backend

---

## [INFO] **Task Disponibili**

### [INFO] **Task di Test e Diagnostica**

```bash
# Test configurazione generale
python devika.py test_config

# Test gestione automatica modelli (NUOVO!)
python devika.py test_model_management

# Test integrazioni specifiche
python devika.py test_whisper          # Test trascrizione audio
python devika.py test_ollama           # Test Ollama LLM
python devika.py test_huggingface      # Test HuggingFace NLP
python devika.py test_lmstudio         # Test LM Studio LLM

# Test integrazione generale
python devika.py test_integrations     # Test completo sistema
```

### ⚡ **Task di Benchmark e Performance**

```bash
# Benchmark completo LLM (MIGLIORATO!)
python devika.py benchmark_llm

# Test agenti AI
python devika.py test_agents

# Test logica di retry
python devika.py retry_logic
```

### [INFO] **Task di Manutenzione**

```bash
# Salvataggio dati CSV
python devika.py export_csv

# Controllo salute sistema
python devika.py system_health

# Manutenzione automatica
python devika.py auto_maintenance

# Refactoring prompt
python devika.py refactor_prompt
```

---

## [INFO] **Nuove Funzionalità di Gestione Modelli**

### 🤖 **LM Studio - Gestione Automatica**

Il sistema ora supporta:

- **[INFO] Rilevamento Automatico**: Trova automaticamente la directory modelli LM Studio
- **[INFO] Download Istruzioni**: Fornisce link diretti a Hugging Face per modelli mancanti
- **[INFO] Avvio Automatico**: Tenta di aprire LM Studio per caricamento manuale
- **[INFO] Guide Dettagliate**: Istruzioni passo-passo per ogni modello

**Modelli Supportati:**
- `mistral` → TheBloke/Mistral-7B-Instruct-v0.2-GGUF
- `llama2` → TheBloke/Llama-2-7B-Chat-GGUF
- `llama3` → TheBloke/Llama-3-8B-Instruct-GGUF
- `gemma` → TheBloke/gemma-2b-it-GGUF
- `codellama` → TheBloke/CodeLlama-7B-Instruct-GGUF

### 🐙 **Ollama - Gestione Automatica**

Il sistema ora supporta:

- **[INFO] Download Automatico**: Usa `ollama pull` per scaricare modelli mancanti
- **[INFO] Verifica Disponibilità**: Controlla automaticamente i modelli installati
- **[INFO] Avvio Server**: Tenta di avviare il server Ollama se non attivo
- **[INFO] Istruzioni Manuali**: Guide per setup manuale quando necessario

**Comandi Automatici:**
```bash
ollama pull mistral
ollama pull llama2
ollama pull codellama
```

---

## [INFO] **Router LLM Intelligente**

### ✨ **Caratteristiche del Router**

- **🎯 Selezione Automatica**: Sceglie il miglior backend disponibile
- **[INFO] Fallback Intelligente**: Passa automaticamente a backend alternativi
- **[REPORT] Monitoraggio Status**: Controlla continuamente la disponibilità
- **[INFO] Gestione Modelli**: Verifica e gestisce modelli per ogni backend

### [INFO] **Configurazione Router**

```yaml
# config_integrations.yaml
llm:
  preferred_backend: "lmstudio"  # lmstudio, ollama, openai
  fallback_strategy: "auto"      # auto, manual, none
  
  lmstudio:
    base_url: "http://localhost:1234/v1/chat/completions"
    model: "mistral"
    timeout: 30
    max_retries: 3
  
  ollama:
    base_url: "http://localhost:11434"
    model: "mistral"
    timeout: 30
    max_retries: 3
```

---

## [INFO] **Test di Gestione Modelli**

### [INFO] **Nuovo Task: test_model_management**

```bash
python devika.py test_model_management
```

**Cosa Testa:**
- [OK] Verifica disponibilità modelli in tutti i backend
- [INFO] Test download automatico modelli
- [INFO] Generazione istruzioni manuali
- [INFO] Test router con gestione modelli
- [REPORT] Report dettagliato con raccomandazioni

**Output Esempio:**
```
[INFO] Testing Automatic Model Management...
============================================================

🤖 Testing LMSTUDIO Backend:
   [INFO] Testing model: mistral
      [OK] Available
      [INFO] Actions: Model already loaded
   
   [INFO] Testing model: llama3
      [WARN]️  Not available
      [INFO] Instructions available (8 steps)
      [INFO] Download Instructions:
         1. [INFO] Download Llama 3 8B Instruct:
         2. [INFO] https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF
         3. [INFO] Steps:
         4. 1. Click the link above
         5. 2. Download the .gguf file (choose appropriate size)

🏆 Overall Summary:
============================================================
🤖 LMSTUDIO: 1/5 models available (20.0%)
🤖 OLLAMA: 3/5 models available (60.0%)

💡 Recommendations:
   [WARN]️  LMSTUDIO: Consider downloading more models
   [REPORT] OLLAMA: Moderate model coverage
```

---

## [INFO] **Utilizzo Avanzato**

### [INFO] **Gestione Modelli Manuale**

```python
from utils.llm_router import create_llm_router

# Crea router
router = create_llm_router()

# Verifica modello specifico
status = router.ensure_model("llama3", "lmstudio")
if not status["success"]:
    print("Istruzioni per download:")
    for instruction in status["instructions"]:
        print(f"  {instruction}")

# Richiesta con verifica automatica modello
response = router.ask("Ciao!", model="mistral")
```

### [REPORT] **Benchmark Avanzato**

```bash
# Benchmark con gestione modelli
python devika.py benchmark_llm
```

**Output Migliorato:**
```
⚡ LLM Backend Benchmark Comparison (Enhanced)...
============================================================

[REPORT] Router Status:
   Current Backend: lmstudio
   Available Backends: ['lmstudio', 'ollama']
   lmstudio: [OK] Available
     Models: mistral, llama2
   ollama: [OK] Available
     Models: mistral, codellama, neural-chat

🏆 Performance Comparison:
============================================================
⚡ Fastest: OLLAMA
🛡️  Most Reliable: LMSTUDIO
🎯 Best Overall: OLLAMA

[REPORT] Detailed Performance:
   LMSTUDIO: 100.0% success, 2.34s avg
   OLLAMA: 100.0% success, 1.87s avg
```

---

## [INFO] **Struttura File**

```
devika_tokintel/
├── tasks/
│   ├── test_model_management.py    # [INFO] Test gestione modelli
│   ├── benchmark_llm.py            # ⚡ Benchmark migliorato
│   ├── test_lmstudio.py            # Test LM Studio
│   ├── test_ollama.py              # Test Ollama
│   └── task_runner.py              # Runner aggiornato
├── logs/
│   ├── model_management_test_*.json # Report gestione modelli
│   └── benchmark_results_*.json     # Report benchmark
└── README_Devika.md                # Documentazione aggiornata
```

---

## 🎯 **Prossimi Passi**

### [OK] **Completato**
- [x] Gestione automatica modelli LM Studio
- [x] Gestione automatica modelli Ollama
- [x] Router LLM intelligente
- [x] Benchmark avanzato
- [x] Test di gestione modelli
- [x] Documentazione completa

### [INFO] **In Sviluppo**
- [ ] Integrazione OpenAI
- [ ] Gestione modelli cloud
- [ ] Interfaccia web Streamlit
- [ ] Configurazione automatica server

---

## 💡 **Suggerimenti**

1. **[INFO] Configurazione Iniziale**: Esegui `test_model_management` per verificare lo stato dei modelli
2. **[INFO] Download Modelli**: Segui le istruzioni automatiche per scaricare modelli mancanti
3. **⚡ Benchmark Regolare**: Usa `benchmark_llm` per monitorare le performance
4. **[INFO] Aggiornamenti**: Mantieni aggiornati i modelli per le migliori performance

---

## 🆘 **Supporto**

Per problemi o domande:
1. Esegui `python devika.py system_health` per diagnostica
2. Controlla i log in `logs/` per dettagli errori
3. Verifica la configurazione in `config_integrations.yaml`
4. Testa singoli componenti con i task specifici
