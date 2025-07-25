#!/bin/bash

# TokIntel v2.1 - Script di Installazione
# Preparazione ambiente di sviluppo

set -e

echo "🔧 Installazione TokIntel v2.1..."

# Verifica sistema
echo "📋 Verifica prerequisiti..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installa Python 3.8+"
    exit 1
fi

# FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg non trovato. Installa FFmpeg per elaborazione video"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   macOS: brew install ffmpeg"
    echo "   Windows: https://ffmpeg.org/download.html"
fi

# Git
if ! command -v git &> /dev/null; then
    echo "⚠️  Git non trovato. Installa Git per versioning"
fi

# Creazione ambiente virtuale
echo "🐍 Creazione ambiente virtuale..."
python3 -m venv .venv

# Attivazione ambiente
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Aggiornamento pip..."
pip install --upgrade pip

# Installazione dipendenze core
echo "📦 Installazione dipendenze core..."
pip install -r requirements.txt

# Installazione dipendenze sviluppo (opzionale)
if [ -f "requirements_dev.txt" ]; then
    echo "🔧 Installazione dipendenze sviluppo..."
    pip install -r requirements_dev.txt
fi

# Installazione pre-commit hooks
if command -v pre-commit &> /dev/null; then
    echo "🔒 Installazione pre-commit hooks..."
    pre-commit install
fi

# Configurazione iniziale
if [ ! -f "config.yaml" ]; then
    echo "⚙️  Creazione configurazione iniziale..."
    cp config.yaml.example config.yaml
    echo "✅ Configurazione creata. Modifica config.yaml con le tue impostazioni"
fi

# Verifica installazione
echo "✅ Verifica installazione..."
python -c "import streamlit, opencv, pydantic; print('✅ Dipendenze installate correttamente')"

echo ""
echo "🎉 Installazione completata!"
echo "🚀 Per avviare: ./run.sh"
echo "📚 Documentazione: README.md"
echo "🔧 Configurazione: config.yaml" 