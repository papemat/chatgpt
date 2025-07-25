# TokIntel v2 - Integrazioni Avanzate

## 🎯 Panoramica

TokIntel v2 ora include tre integrazioni avanzate per potenziare l'analisi di contenuti multimediali:

1. **🎤 Whisper** - Trascrizione audio/video
2. **🤖 Ollama** - LLM locali
3. **🤗 HuggingFace** - Task NLP avanzati

## [INFO] Installazione

### Setup Completo
```bash
# Clona il repository
git clone <repository-url>
cd TokIntel_v2

# Installa dipendenze complete
pip install -r requirements_integrations.txt

# Setup Devika (assistente AI)
cd ../devika_tokintel
python setup.py
```

### Setup Selettivo

#### Solo Whisper
```bash
pip install openai-whisper ffmpeg-python
```

#### Solo Ollama
```bash
# Installa Ollama da https://ollama.ai
pip install requests
```

#### Solo HuggingFace
```bash
pip install transformers torch accelerate
```

## 🎤 Whisper Integration

### Caratteristiche
- [OK] Trascrizione audio e video
- [OK] Supporto locale e API
- [OK] Estrazione automatica audio da video
- [OK] Fallback automatico
- [OK] Batch processing
- [OK] Ottimizzazione GPU

### Configurazione
```yaml
whisper:
  use_local: true
  use_api: false
  model_size: "base"  # tiny, base, small, medium, large
  device: "auto"
  batch_size: 16
```

### Utilizzo
```python
from audio.whisper_transcriber import create_transcriber

# Crea transcriber
transcriber = create_transcriber({
    'use_local': True,
    'model_size': 'base'
})

# Trascrivi file
result = transcriber.transcribe("video.mp4")
print(result['text'])
```

### Test con Devika
```bash
cd devika_tokintel
python devika.py test_whisper
```

## 🤖 Ollama Integration

### Caratteristiche
- [OK] LLM locali (Mistral, LLaMA, CodeLlama)
- [OK] Chat completions
- [OK] Embeddings
- [OK] Benchmark automatico
- [OK] Retry logic
- [OK] Multi-modello support

### Configurazione
```yaml
ollama:
  base_url: "http://localhost:11434"
  default_model: "mistral"
  timeout: 30
  temperature: 0.7
```

### Utilizzo
```python
from llm.ollama_client import create_ollama_client

# Crea client
client = create_ollama_client({
    'default_model': 'mistral'
})

# Genera testo
result = client.generate("Explain AI")
print(result['text'])

# Chat
messages = [{"role": "user", "content": "Hello"}]
result = client.chat(messages)
```

### Test con Devika
```bash
cd devika_tokintel
python devika.py test_ollama
```

## 🤗 HuggingFace Integration

### Caratteristiche
- [OK] Summarization
- [OK] Sentiment analysis
- [OK] Named Entity Recognition (NER)
- [OK] Keyword extraction
- [OK] Text classification
- [OK] Translation
- [OK] Question answering

### Configurazione
```yaml
huggingface:
  device: "auto"
  use_gpu: true
  models:
    summarization: "facebook/bart-large-cnn"
    sentiment: "cardiffnlp/twitter-roberta-base-sentiment-latest"
    ner: "dbmdz/bert-large-cased-finetuned-conll03-english"
```

### Utilizzo
```python
from huggingface.inference import create_hf_inference

# Crea inference engine
hf = create_hf_inference({
    'use_gpu': True
})

# Summarization
result = hf.summarize("Long text...")
print(result['summary'])

# Sentiment analysis
result = hf.analyze_sentiment("I love this!")
print(result['top_prediction']['label'])

# NER
result = hf.extract_entities("Apple CEO Tim Cook...")
print(result['entities'])
```

### Test con Devika
```bash
cd devika_tokintel
python devika.py test_huggingface
```

## [INFO] Configurazione Avanzata

### Pipeline Completa
```yaml
pipeline:
  audio_extraction: true
  transcription: true
  summarization: true
  sentiment_analysis: true
  keyword_extraction: true
  local_llm: true
  cloud_llm: true
  fallback_strategy: "local_first"
```

### Performance
```yaml
performance:
  parallel_processing: true
  max_workers: 4
  memory_limit: "4GB"
  gpu_memory_fraction: 0.8
```

### Quality Settings
```yaml
quality:
  transcription_confidence_threshold: 0.8
  sentiment_confidence_threshold: 0.7
  summary_min_length: 30
  summary_max_length: 200
```

## [INFO] Testing e Benchmarking

### Test Completo
```bash
# Test tutte le integrazioni
cd devika_tokintel
python devika.py test_integrations

# Test specifici
python devika.py test_whisper
python devika.py test_ollama
python devika.py test_huggingface
```

### Benchmark
```python
# Whisper benchmark
transcriber.batch_transcribe(files)

# Ollama benchmark
client.benchmark_model('mistral', prompts)

# HuggingFace benchmark
hf.benchmark_pipeline('sentiment', texts)
```

## [REPORT] Monitoraggio

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)

# Tutti i moduli loggano automaticamente
# - Processing times
# - Errors and warnings
# - Performance metrics
```

### Metrics
```yaml
monitoring:
  enable_metrics: true
  log_processing_times: true
  save_intermediate_results: true
  performance_benchmarking: true
```

## [INFO] Esempi Pratici

### Analisi Video Completa
```python
from audio.whisper_transcriber import create_transcriber
from huggingface.inference import create_hf_inference
from llm.ollama_client import create_ollama_client

# 1. Trascrivi video
transcriber = create_transcriber()
transcription = transcriber.transcribe("video.mp4")

# 2. Analizza testo
hf = create_hf_inference()
summary = hf.summarize(transcription['text'])
sentiment = hf.analyze_sentiment(transcription['text'])
keywords = hf.extract_keywords(transcription['text'])

# 3. Genera insights con LLM locale
client = create_ollama_client()
prompt = f"Analizza questo contenuto: {summary['summary']}"
insights = client.generate(prompt)

print(f"Video: {transcription['text']}")
print(f"Riassunto: {summary['summary']}")
print(f"Sentiment: {sentiment['top_prediction']['label']}")
print(f"Keywords: {[k['text'] for k in keywords['keywords']]}")
print(f"Insights: {insights['text']}")
```

### Batch Processing
```python
# Processa multiple files
files = ["video1.mp4", "video2.mp4", "audio1.wav"]

# Trascrizione batch
transcriptions = transcriber.batch_transcribe(files)

# Analisi batch
for trans in transcriptions:
    if 'error' not in trans:
        summary = hf.summarize(trans['text'])
        sentiment = hf.analyze_sentiment(trans['text'])
        # Salva risultati...
```

## [INFO] Troubleshooting

### Whisper Issues
```bash
# Verifica FFmpeg
ffmpeg -version

# Reinstalla Whisper
pip uninstall openai-whisper
pip install openai-whisper

# Verifica GPU
python -c "import torch; print(torch.cuda.is_available())"
```

### Ollama Issues
```bash
# Verifica server
curl http://localhost:11434/api/tags

# Riavvia server
ollama serve

# Verifica modelli
ollama list
```

### HuggingFace Issues
```bash
# Verifica CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Clear cache
rm -rf ~/.cache/huggingface/

# Reinstalla transformers
pip install --upgrade transformers torch
```

## [REPORT] Performance Tips

### Whisper
- Usa `model_size: "base"` per bilanciare velocità/qualità
- Abilita GPU per accelerazione
- Usa batch processing per multiple files

### Ollama
- Usa modelli più piccoli per velocità
- Configura timeout appropriati
- Usa retry logic per stabilità

### HuggingFace
- Usa GPU quando disponibile
- Configura batch_size appropriato
- Cache models per riutilizzo

## 🤝 Contributi

Per contribuire alle integrazioni:

1. Fork il repository
2. Crea feature branch
3. Implementa e testa
4. Aggiungi test Devika
5. Submit pull request

## [INFO] Licenza

Questo progetto è sotto licenza MIT. Vedi LICENSE per dettagli.

## 🆘 Supporto

- [INFO] Email: support@tokintel.com
- 💬 Discord: [TokIntel Community]
- [INFO] Docs: [Documentazione Completa]
- 🐛 Issues: [GitHub Issues] 