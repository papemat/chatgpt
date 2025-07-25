#!/bin/bash

# TokIntel v2.1 - Enterprise Grade
# Script di avvio automatico

echo "🚀 Avvio TokIntel v2.1..."

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installa Python 3.8+"
    exit 1
fi

# Verifica dipendenze
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt non trovato"
    exit 1
fi

# Installa dipendenze se necessario
if [ ! -d ".venv" ]; then
    echo "📦 Creazione ambiente virtuale..."
    python3 -m venv .venv
fi

# Attiva ambiente virtuale
source .venv/bin/activate

# Installa/aggiorna dipendenze
echo "📦 Installazione dipendenze..."
pip install -r requirements.txt

# Verifica configurazione
if [ ! -f "config.yaml" ]; then
    echo "⚙️ Copia configurazione di esempio..."
    cp config.yaml.example config.yaml
    echo "⚠️  Modifica config.yaml con le tue impostazioni"
fi

# Avvia Streamlit
echo "🎨 Avvio interfaccia Streamlit..."
streamlit run ui/interface.py --server.port 8501 --server.address 0.0.0.0 