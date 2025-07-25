#!/bin/bash
# TokIntel v2 - TikTok Integration Setup Script

set -e

echo "🎵 TokIntel v2 - Setup Integrazione TikTok"
echo "=========================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per log colorato
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica Python
log_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 non trovato. Installa Python 3.8+ prima di continuare."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_success "Python $PYTHON_VERSION trovato"

# Verifica pip
log_info "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    log_error "pip3 non trovato. Installa pip prima di continuare."
    exit 1
fi

log_success "pip3 trovato"

# Installa dipendenze Python
log_info "Installando dipendenze Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    log_success "Dipendenze Python installate"
else
    log_error "Errore nell'installazione delle dipendenze Python"
    exit 1
fi

# Installa Playwright
log_info "Installando Playwright..."
python3 -m playwright install chromium

if [ $? -eq 0 ]; then
    log_success "Playwright installato"
else
    log_error "Errore nell'installazione di Playwright"
    exit 1
fi

# Installa dipendenze di sistema per Playwright
log_info "Installando dipendenze di sistema per Playwright..."
python3 -m playwright install-deps

if [ $? -eq 0 ]; then
    log_success "Dipendenze di sistema installate"
else
    log_warning "Alcune dipendenze di sistema potrebbero non essere installate correttamente"
fi

# Crea directory necessarie
log_info "Creando directory necessarie..."
mkdir -p config
mkdir -p logs
mkdir -p output

log_success "Directory create"

# Crea file di configurazione se non esiste
if [ ! -f "config/config.yaml" ]; then
    log_info "Creando file di configurazione..."
    cp config.yaml.example config/config.yaml
    log_success "File di configurazione creato"
    log_warning "Modifica config/config.yaml con le tue credenziali TikTok"
else
    log_info "File di configurazione già esistente"
fi

# Verifica installazione
log_info "Verificando installazione..."

# Test import moduli
python3 -c "
try:
    import playwright
    print('✓ Playwright importato correttamente')
except ImportError as e:
    print(f'✗ Errore import Playwright: {e}')
    exit(1)

try:
    import cryptography
    print('✓ Cryptography importato correttamente')
except ImportError as e:
    print(f'✗ Errore import Cryptography: {e}')
    exit(1)

try:
    import yaml
    print('✓ PyYAML importato correttamente')
except ImportError as e:
    print(f'✗ Errore import PyYAML: {e}')
    exit(1)

print('✓ Tutti i moduli importati correttamente')
"

if [ $? -eq 0 ]; then
    log_success "Verifica installazione completata"
else
    log_error "Errore nella verifica installazione"
    exit 1
fi

# Test Playwright browser
log_info "Testando browser Playwright..."
python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def test_browser():
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.tiktok.com')
        await browser.close()
        await playwright.stop()
        print('✓ Browser Playwright funzionante')
    except Exception as e:
        print(f'✗ Errore browser Playwright: {e}')
        exit(1)

asyncio.run(test_browser())
"

if [ $? -eq 0 ]; then
    log_success "Test browser completato"
else
    log_error "Errore nel test browser"
    exit 1
fi

# Mostra istruzioni finali
echo ""
echo "🎉 Setup completato con successo!"
echo "================================"
echo ""
echo "📋 Prossimi passi:"
echo ""
echo "1. 📝 Configura le credenziali TikTok:"
echo "   - Vai su https://developers.tiktok.com/"
echo "   - Crea una nuova app"
echo "   - Modifica config/config.yaml con le tue credenziali"
echo ""
echo "2. 🚀 Avvia l'interfaccia TikTok:"
echo "   streamlit run ui/import_tiktok.py"
echo ""
echo "3. 📚 Leggi la documentazione:"
echo "   cat TIKTOK_INTEGRATION.md"
echo ""
echo "4. 🔧 Configurazione avanzata:"
echo "   - Modifica config/config.yaml per personalizzare"
echo "   - Controlla logs/ per debugging"
echo ""
echo "⚠️  Note importanti:"
echo "   - Rispetta i Terms of Service di TikTok"
echo "   - Usa solo le API ufficiali"
echo "   - Non condividere le tue credenziali"
echo ""
echo "📞 Supporto:"
echo "   - GitHub Issues: https://github.com/your-repo/issues"
echo "   - Documentazione: TIKTOK_INTEGRATION.md"
echo ""

log_success "Setup completato! 🎵" 