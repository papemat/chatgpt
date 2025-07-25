#!/bin/bash

# 🚀 TokIntel v2.1 Pro+ Launcher
# Script per lanciare le funzionalità avanzate

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

# Controllo prerequisiti
check_requirements() {
    print_status "Controllo prerequisiti..."
    
    # Controllo Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 non trovato. Installa Python 3.8+"
        exit 1
    fi
    
    # Controllo pip
    if ! command -v pip &> /dev/null; then
        print_error "pip non trovato. Installa pip"
        exit 1
    fi
    
    # Controllo virtual environment
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment non attivo. Consigliato attivarlo."
    fi
    
    print_success "Prerequisiti verificati"
}

# Installazione dipendenze Pro
install_pro_dependencies() {
    print_status "Installazione dipendenze Pro..."
    
    if [ -f "requirements_pro.txt" ]; then
        pip install -r requirements_pro.txt
        print_success "Dipendenze Pro installate"
    else
        print_error "File requirements_pro.txt non trovato"
        exit 1
    fi
}

# Inizializzazione database
init_database() {
    print_status "Inizializzazione database..."
    
    # Controllo se PostgreSQL è configurato
    if [ -z "$DB_HOST" ] && [ -z "$DATABASE_URL" ]; then
        print_warning "Database PostgreSQL non configurato. Usando SQLite per test."
        export DATABASE_URL="sqlite:///tokintel_pro.db"
    fi
    
    # Inizializza database
    python3 -c "
from db.database import init_database
import os
db_url = os.getenv('DATABASE_URL', 'sqlite:///tokintel_pro.db')
init_database(db_url)
print('Database inizializzato con successo')
"
    
    print_success "Database inizializzato"
}

# Menu principale
show_menu() {
    echo ""
    echo "🎯 TokIntel v2.1 Pro+ - Menu Principale"
    echo "======================================"
    echo "1. 🎥 Analisi Video (Core)"
    echo "2. 💬 Chat con Agenti AI"
    echo "3. 📊 Dashboard Analytics"
    echo "4. 📈 Genera Report PDF"
    echo "5. 🔧 Gestione Database"
    echo "6. 🚀 API REST Server"
    echo "7. 📋 Cronologia Analisi"
    echo "8. ⚙️  Configurazione"
    echo "9. 🧪 Test Sistema"
    echo "0. ❌ Esci"
    echo ""
}

# Funzioni per ogni opzione
run_video_analysis() {
    print_status "Avvio analisi video..."
    streamlit run ui/interface.py --server.port 8501
}

run_chat_agents() {
    print_status "Avvio chat con agenti AI..."
    streamlit run ui/chat_agents.py --server.port 8502
}

run_analytics() {
    print_status "Avvio dashboard analytics..."
    streamlit run ui/analytics.py --server.port 8503
}

generate_pdf_report() {
    print_status "Generazione report PDF di esempio..."
    python3 -c "
from utils.pdf_exporter import create_sample_report
output_file = create_sample_report()
print(f'Report generato: {output_file}')
"
}

manage_database() {
    echo ""
    echo "🗄️  Gestione Database"
    echo "===================="
    echo "1. Inizializza database"
    echo "2. Backup database"
    echo "3. Ripristina database"
    echo "4. Statistiche database"
    echo "0. Torna al menu principale"
    echo ""
    
    read -p "Scelta: " db_choice
    
    case $db_choice in
        1) init_database ;;
        2) print_status "Backup database..." ;;
        3) print_status "Ripristino database..." ;;
        4) print_status "Statistiche database..." ;;
        0) return ;;
        *) print_error "Scelta non valida" ;;
    esac
}

run_api_server() {
    print_status "Avvio API REST server..."
    uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
}

show_analysis_history() {
    print_status "Recupero cronologia analisi..."
    python3 -c "
from db.database import get_analysis_history
history = get_analysis_history(limit=10)
print('\\n📋 Ultime 10 Analisi:')
print('=' * 50)
for i, analysis in enumerate(history, 1):
    print(f'{i}. {analysis[\"title\"]} (Score: {analysis[\"score\"]})')
    print(f'   Data: {analysis[\"created_at\"]}')
    print(f'   Sintesi: {analysis[\"summary\"][:100]}...')
    print()
"
}

show_configuration() {
    echo ""
    echo "⚙️  Configurazione Sistema"
    echo "========================="
    echo "1. Modifica config.yaml"
    echo "2. Configura database"
    echo "3. Configura API keys"
    echo "4. Verifica configurazione"
    echo "0. Torna al menu principale"
    echo ""
    
    read -p "Scelta: " config_choice
    
    case $config_choice in
        1) 
            if command -v nano &> /dev/null; then
                nano config.yaml
            elif command -v vim &> /dev/null; then
                vim config.yaml
            else
                print_error "Editor non trovato. Modifica manualmente config.yaml"
            fi
            ;;
        2) print_status "Configurazione database..." ;;
        3) print_status "Configurazione API keys..." ;;
        4) print_status "Verifica configurazione..." ;;
        0) return ;;
        *) print_error "Scelta non valida" ;;
    esac
}

run_system_tests() {
    print_status "Esecuzione test sistema..."
    
    # Test database
    print_status "Test database..."
    python3 -c "
from db.database import init_database
try:
    db = init_database('sqlite:///test.db')
    print('✅ Database: OK')
except Exception as e:
    print(f'❌ Database: ERRORE - {e}')
"
    
    # Test PDF exporter
    print_status "Test PDF exporter..."
    python3 -c "
from utils.pdf_exporter import create_sample_report
try:
    output = create_sample_report()
    print(f'✅ PDF Exporter: OK - {output}')
except Exception as e:
    print(f'❌ PDF Exporter: ERRORE - {e}')
"
    
    # Test chat agents
    print_status "Test chat agents..."
    python3 -c "
from ui.chat_agents import AgentChat
try:
    chat = AgentChat()
    response = chat.get_agent_response('strategist', 'test')
    print('✅ Chat Agents: OK')
except Exception as e:
    print(f'❌ Chat Agents: ERRORE - {e}')
"
    
    print_success "Test completati"
}

# Funzione principale
main() {
    echo "🎯 TokIntel v2.1 Pro+"
    echo "====================="
    
    # Controllo prerequisiti
    check_requirements
    
    # Installazione dipendenze se richiesto
    if [ "$1" = "--install" ]; then
        install_pro_dependencies
        init_database
        print_success "Installazione completata!"
        exit 0
    fi
    
    # Loop principale
    while true; do
        show_menu
        read -p "Scelta: " choice
        
        case $choice in
            1) run_video_analysis ;;
            2) run_chat_agents ;;
            3) run_analytics ;;
            4) generate_pdf_report ;;
            5) manage_database ;;
            6) run_api_server ;;
            7) show_analysis_history ;;
            8) show_configuration ;;
            9) run_system_tests ;;
            0) 
                print_success "Arrivederci!"
                exit 0
                ;;
            *) print_error "Scelta non valida" ;;
        esac
        
        echo ""
        read -p "Premi ENTER per continuare..."
    done
}

# Gestione argomenti
case "$1" in
    --install)
        main --install
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --install    Installa dipendenze e inizializza database"
        echo "  --help, -h   Mostra questo messaggio"
        echo ""
        echo "Esempi:"
        echo "  $0              # Avvia menu interattivo"
        echo "  $0 --install    # Installa tutto"
        ;;
    *)
        main "$@"
        ;;
esac 