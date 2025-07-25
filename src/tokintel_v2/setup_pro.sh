#!/bin/bash

# 🚀 TokIntel v2.1 Pro+ Setup Script
# Script completo per installazione e configurazione

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funzioni per output colorato
print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                    TokIntel v2.1 Pro+ Setup                  ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Variabili di configurazione
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_NAME="tokintel_pro_env"
PYTHON_VERSION="3.8"

# Funzione per controllare prerequisiti
check_prerequisites() {
    print_step "Controllo prerequisiti..."
    
    # Controllo Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 non trovato. Installa Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION_CHECK=$(python3 -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
    if [[ $(echo "$PYTHON_VERSION_CHECK < $PYTHON_VERSION" | bc -l) -eq 1 ]]; then
        print_error "Python $PYTHON_VERSION_CHECK trovato. Richiesto Python $PYTHON_VERSION+"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION_CHECK trovato"
    
    # Controllo pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 non trovato. Installa pip"
        exit 1
    fi
    
    print_success "pip3 trovato"
    
    # Controllo git
    if ! command -v git &> /dev/null; then
        print_warning "git non trovato. Consigliato per versioning"
    else
        print_success "git trovato"
    fi
    
    # Controllo FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        print_warning "FFmpeg non trovato. Richiesto per elaborazione video"
        print_info "Installa con: sudo apt install ffmpeg (Ubuntu/Debian)"
    else
        print_success "FFmpeg trovato"
    fi
}

# Funzione per creare virtual environment
create_virtual_environment() {
    print_step "Creazione virtual environment..."
    
    if [ -d "$VENV_NAME" ]; then
        print_warning "Virtual environment già esistente. Rimuovo..."
        rm -rf "$VENV_NAME"
    fi
    
    python3 -m venv "$VENV_NAME"
    print_success "Virtual environment creato: $VENV_NAME"
    
    # Attiva virtual environment
    source "$VENV_NAME/bin/activate"
    print_success "Virtual environment attivato"
}

# Funzione per aggiornare pip
upgrade_pip() {
    print_step "Aggiornamento pip..."
    pip install --upgrade pip
    print_success "pip aggiornato"
}

# Funzione per installare dipendenze base
install_base_dependencies() {
    print_step "Installazione dipendenze base..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dipendenze base installate"
    else
        print_error "File requirements.txt non trovato"
        exit 1
    fi
}

# Funzione per installare dipendenze Pro
install_pro_dependencies() {
    print_step "Installazione dipendenze Pro..."
    
    if [ -f "requirements_pro.txt" ]; then
        pip install -r requirements_pro.txt
        print_success "Dipendenze Pro installate"
    else
        print_error "File requirements_pro.txt non trovato"
        exit 1
    fi
}

# Funzione per configurare database
setup_database() {
    print_step "Configurazione database..."
    
    # Crea file di configurazione se non esiste
    if [ ! -f "config.yaml" ]; then
        if [ -f "config.yaml.example" ]; then
            cp config.yaml.example config.yaml
            print_success "File config.yaml creato da esempio"
        else
            print_warning "File config.yaml non trovato. Crea manualmente"
        fi
    fi
    
    # Inizializza database SQLite per test
    python3 -c "
from db.database import init_database
try:
    db = init_database('sqlite:///tokintel_pro.db')
    print('Database SQLite inizializzato con successo')
except Exception as e:
    print(f'Errore inizializzazione database: {e}')
"
    
    print_success "Database configurato"
}

# Funzione per testare installazione
test_installation() {
    print_step "Test installazione..."
    
    # Test import moduli
    python3 -c "
modules = [
    'streamlit',
    'plotly',
    'pandas',
    'numpy',
    'fpdf',
    'sqlalchemy'
]

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}: OK')
    except ImportError as e:
        print(f'❌ {module}: ERRORE - {e}')
"
    
    # Test funzionalità Pro
    python3 -c "
try:
    from ui.chat_agents import AgentChat
    from utils.pdf_exporter import PDFExporter
    from db.database import DatabaseManager
    print('✅ Funzionalità Pro: OK')
except ImportError as e:
    print(f'❌ Funzionalità Pro: ERRORE - {e}')
"
    
    print_success "Test completati"
}

# Funzione per creare script di avvio
create_launch_scripts() {
    print_step "Creazione script di avvio..."
    
    # Script per attivare virtual environment e lanciare
    cat > launch_pro.sh << 'EOF'
#!/bin/bash
# Script per lanciare TokIntel Pro

# Attiva virtual environment
source tokintel_pro_env/bin/activate

# Lancia la dashboard Pro
streamlit run ui/pro_dashboard.py --server.port 8501
EOF
    
    chmod +x launch_pro.sh
    
    # Script per chat agents
    cat > launch_chat.sh << 'EOF'
#!/bin/bash
# Script per lanciare chat agents

# Attiva virtual environment
source tokintel_pro_env/bin/activate

# Lancia chat agents
streamlit run ui/chat_agents.py --server.port 8502
EOF
    
    chmod +x launch_chat.sh
    
    # Script per analytics
    cat > launch_analytics.sh << 'EOF'
#!/bin/bash
# Script per lanciare analytics

# Attiva virtual environment
source tokintel_pro_env/bin/activate

# Lancia analytics
streamlit run ui/analytics.py --server.port 8503
EOF
    
    chmod +x launch_analytics.sh
    
    print_success "Script di avvio creati"
}

# Funzione per eseguire test completi
run_comprehensive_tests() {
    print_step "Esecuzione test completi..."
    
    # Test database
    python3 -c "
from db.database import init_database
try:
    db = init_database('sqlite:///test_setup.db')
    print('✅ Database: OK')
except Exception as e:
    print(f'❌ Database: ERRORE - {e}')
"
    
    # Test PDF exporter
    python3 -c "
from utils.pdf_exporter import create_sample_report
try:
    output = create_sample_report()
    print(f'✅ PDF Exporter: OK - {output}')
except Exception as e:
    print(f'❌ PDF Exporter: ERRORE - {e}')
"
    
    # Test chat agents
    python3 -c "
from ui.chat_agents import AgentChat
try:
    chat = AgentChat()
    response = chat.get_agent_response('strategist', 'test')
    print('✅ Chat Agents: OK')
except Exception as e:
    print(f'❌ Chat Agents: ERRORE - {e}')
"
    
    print_success "Test completi eseguiti"
}

# Funzione per mostrare informazioni finali
show_final_info() {
    print_header
    echo ""
    print_success "🎉 Installazione TokIntel v2.1 Pro+ completata!"
    echo ""
    print_info "📁 Directory progetto: $PROJECT_DIR"
    print_info "🐍 Virtual environment: $VENV_NAME"
    print_info "📊 Database: tokintel_pro.db"
    echo ""
    print_info "🚀 Comandi disponibili:"
    echo "   ./launch_pro.sh      - Dashboard Pro completa"
    echo "   ./launch_chat.sh     - Chat con Agenti AI"
    echo "   ./launch_analytics.sh - Analytics avanzati"
    echo "   ./run_pro.sh         - Menu interattivo"
    echo ""
    print_info "📚 Documentazione:"
    echo "   NOVITA_PRO.md        - Guida funzionalità Pro"
    echo "   README.md            - Documentazione generale"
    echo ""
    print_info "🔧 Configurazione:"
    echo "   config.yaml          - Configurazione principale"
    echo "   .env                 - Variabili ambiente (opzionale)"
    echo ""
    print_warning "⚠️  Ricorda di attivare il virtual environment:"
    echo "   source $VENV_NAME/bin/activate"
    echo ""
    print_success "🎯 Pronto per lanciare TokIntel Pro+!"
}

# Funzione per pulizia
cleanup() {
    print_step "Pulizia file temporanei..."
    
    # Rimuovi file di test
    rm -f test_setup.db
    rm -f sample_report.pdf
    
    print_success "Pulizia completata"
}

# Funzione principale
main() {
    print_header
    
    # Controllo argomenti
    case "${1:-}" in
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --help, -h     Mostra questo messaggio"
            echo "  --test-only    Esegui solo i test"
            echo "  --clean        Pulisci installazione precedente"
            echo ""
            echo "Esempi:"
            echo "  $0              # Installazione completa"
            echo "  $0 --test-only  # Solo test"
            echo "  $0 --clean      # Pulizia e reinstallazione"
            exit 0
            ;;
        --test-only)
            print_info "Modalità test-only"
            test_installation
            run_comprehensive_tests
            exit 0
            ;;
        --clean)
            print_info "Modalità pulizia"
            cleanup
            if [ -d "$VENV_NAME" ]; then
                rm -rf "$VENV_NAME"
                print_success "Virtual environment rimosso"
            fi
            exit 0
            ;;
    esac
    
    # Esegui installazione completa
    check_prerequisites
    create_virtual_environment
    upgrade_pip
    install_base_dependencies
    install_pro_dependencies
    setup_database
    create_launch_scripts
    test_installation
    run_comprehensive_tests
    cleanup
    show_final_info
}

# Gestione errori
trap 'print_error "Errore durante l'installazione. Controlla i log."; exit 1' ERR

# Esegui funzione principale
main "$@" 