# [INFO] TokIntel v2.1 - Guida Deployment Enterprise

## [INFO] Prerequisiti

### **Sistema Operativo**
- [OK] **Linux** (Ubuntu 20.04+, CentOS 7+)
- [OK] **macOS** (10.15+)
- [OK] **Windows** (10/11 con WSL2 raccomandato)

### **Software Richiesto**
- **Python**: 3.8+ (3.9+ raccomandato)
- **FFmpeg**: Per elaborazione video
- **Git**: Per versioning
- **Docker**: Opzionale, per containerizzazione

### **Risorse Minime**
- **RAM**: 4GB (8GB raccomandato)
- **Storage**: 10GB liberi
- **CPU**: 2 core (4+ raccomandato)
- **GPU**: Opzionale (CUDA per accelerazione)

---

## [INFO] Installazione

### **Opzione 1: Installazione Diretta**

```bash
# 1. Clona il repository
git clone https://github.com/yourusername/tokintel-v2.git
cd tokintel-v2

# 2. Usa il pacchetto release
cd release/TokIntel_v2.1

# 3. Esegui installazione automatica
chmod +x install.sh
./install.sh
```

### **Opzione 2: Installazione Manuale**

```bash
# 1. Crea ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oppure
.venv\Scripts\activate     # Windows

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Configura il sistema
cp config.yaml.example config.yaml
# Modifica config.yaml con le tue impostazioni
```

### **Opzione 3: Docker (Raccomandato per Produzione)**

```bash
# 1. Build dell'immagine
docker build -t tokintel-v2.1 .

# 2. Esegui container
docker run -p 8501:8501 -v $(pwd)/data:/app/data tokintel-v2.1
```

---

## ⚙️ Configurazione

### **File di Configurazione**

Modifica `config.yaml` con le tue impostazioni:

```yaml
# Basic settings
model: "gpt-4"                    # Modello LLM
language: "it"                    # Lingua analisi

# API Keys
llm_config:
  api_key: "your-openai-api-key"  # OpenAI API Key
  endpoint: null                   # Endpoint locale (se usi modelli locali)

# Analysis settings
keywords:
  - "motivazione"
  - "hook"
  - "viral"
  - "engagement"

# Output settings
export_format: ["csv", "json"]
output_folder: "output/"
```

### **Variabili d'Ambiente**

```bash
# OpenAI API Key
export OPENAI_API_KEY="your-api-key"

# Logging
export TOKINTEL_LOG_LEVEL="INFO"
export TOKINTEL_LOG_FILE="/var/log/tokintel.log"

# Processing
export TOKINTEL_MAX_VIDEOS=100
export TOKINTEL_TIMEOUT=300
```

---

## [INFO] Avvio del Sistema

### **Interfaccia Web (Raccomandato)**

```bash
# Avvio automatico
chmod +x run.sh
./run.sh

# Oppure manuale
streamlit run ui/interface.py --server.port 8501 --server.address 0.0.0.0
```

**Accesso**: http://localhost:8501

### **CLI (Command Line)**

```bash
# Analisi singolo video
python main.py --video path/to/video.mp4

# Analisi directory
python main.py --directory path/to/videos/

# Modalità batch
python main.py --batch --input-dir videos/ --output-dir results/
```

### **API REST (Se configurata)**

```bash
# Avvia server API
python api/server.py --port 8000

# Test endpoint
curl -X POST http://localhost:8000/analyze \
  -F "video=@video.mp4" \
  -F "config=@config.json"
```

---

## [INFO] Test e Validazione

### **Test di Sistema**

```bash
# Test dipendenze
python -c "import cv2, streamlit, pydantic; print('[OK] OK')"

# Test configurazione
python -c "from core.config import ConfigManager; print('[OK] Config OK')"

# Test logging
python -c "from core.logger import setup_logger; print('[OK] Logger OK')"
```

### **Test Funzionale**

```bash
# Test con video di esempio
python main.py --video samples/test_video.mp4

# Verifica output
ls -la output/
cat output/analysis_results.json
```

### **Test Performance**

```bash
# Test batch processing
python main.py --batch --input-dir test_videos/ --max-workers 4

# Monitoraggio risorse
htop  # o top
```

---

## [REPORT] Monitoraggio

### **Logs**

```bash
# Log in tempo reale
tail -f logs/tokintel.log

# Log per livello
grep "ERROR" logs/tokintel.log
grep "WARNING" logs/tokintel.log
```

### **Metriche**

```bash
# Statistiche elaborazione
python tools/metrics.py --report

# Performance analysis
python tools/performance_analyzer.py
```

### **Health Check**

```bash
# Controllo stato sistema
python tools/health_check.py

# Verifica connettività
python tools/connectivity_test.py
```

---

## [INFO] Troubleshooting

### **Problemi Comuni**

#### **1. Import Errors**
```bash
# Soluzione: Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

#### **2. FFmpeg Non Trovato**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Scarica da https://ffmpeg.org/download.html
```

#### **3. Memory Issues**
```bash
# Riduci batch size
export TOKINTEL_BATCH_SIZE=5

# Aumenta swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### **4. API Rate Limits**
```bash
# Aumenta delay tra richieste
export TOKINTEL_REQUEST_DELAY=2

# Usa retry logic
export TOKINTEL_MAX_RETRIES=5
```

### **Debug Avanzato**

```bash
# Modalità debug
export TOKINTEL_DEBUG=1
python main.py --debug

# Profiling
python -m cProfile -o profile.stats main.py
python tools/profile_analyzer.py profile.stats
```

---

## [INFO] Sicurezza

### **Best Practices**

1. **API Keys**: Mai committare in Git
2. **Firewall**: Limita accesso alle porte necessarie
3. **Updates**: Mantieni aggiornate le dipendenze
4. **Backup**: Backup regolari dei dati
5. **Monitoring**: Monitora accessi e performance

### **Configurazione Sicura**

```yaml
# config.yaml sicuro
llm_config:
  api_key: "${OPENAI_API_KEY}"  # Usa variabili d'ambiente
  timeout: 30
  max_retries: 3

security:
  enable_ssl: true
  allowed_hosts: ["localhost", "your-domain.com"]
  rate_limit: 100  # richieste per minuto
```

---

## [REPORT] Scaling

### **Vertical Scaling**

```bash
# Aumenta risorse
export TOKINTEL_MAX_WORKERS=8
export TOKINTEL_BATCH_SIZE=20
export TOKINTEL_MEMORY_LIMIT=8G
```

### **Horizontal Scaling**

```bash
# Load balancer
docker-compose up --scale tokintel=3

# Kubernetes
kubectl apply -f k8s/tokintel-deployment.yaml
kubectl scale deployment tokintel --replicas=5
```

---

## 🎯 Prossimi Step

### **Immediate (1-2 giorni)**
1. [OK] **Deploy su ambiente di test**
2. [OK] **Test funzionale completo**
3. [OK] **Configurazione monitoring**

### **A Medio Termine (1 settimana)**
1. [INFO] **Training team**
2. [INFO] **Documentazione utente**
3. [INFO] **Processi di backup**

### **A Lungo Termine (1 mese)**
1. [REPORT] **Analisi performance**
2. [REPORT] **Ottimizzazioni**
3. [REPORT] **Pianificazione v2.2**

---

## [INFO] Supporto

### **Documentazione**
- [INFO] **README.md**: Guida generale
- [INFO] **API_DOCS.md**: Documentazione API
- [INFO] **TROUBLESHOOTING.md**: Risoluzione problemi

### **Contatti**
- 🐛 **Issues**: GitHub Issues
- 💬 **Discord**: Server community
- [INFO] **Email**: support@tokintel.com

---

*Guida Deployment TokIntel v2.1 Enterprise*  
*Versione: 2.1.0*  
*Data: 24 Luglio 2025* 