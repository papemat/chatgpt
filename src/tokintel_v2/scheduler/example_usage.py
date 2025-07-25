#!/usr/bin/env python3
"""
[INFO] Esempi di Utilizzo - Auto-Analyze Scheduler
Esempi pratici per utilizzare il modulo scheduler in diversi scenari
"""

import asyncio
import time
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from scheduler import (
    start_auto_analyzer,
    stop_auto_analyzer,
    get_auto_analyzer_status,
    AutoAnalyzeScheduler
)

async def example_basic_usage():
    """Esempio 1: Utilizzo base dello scheduler"""
    print("[INFO] Esempio 1: Utilizzo Base")
    print("-" * 40)
    
    # Avvia scheduler per user_id=1 ogni 30 minuti
    success = start_auto_analyzer(user_id=1, interval_minutes=30)
    
    if success:
        print("[OK] Scheduler avviato con successo")
        
        # Mostra status
        status = get_auto_analyzer_status()
        print(f"[REPORT] Status: {status}")
        
        # Simula esecuzione per 5 secondi
        print("⏳ Esecuzione per 5 secondi...")
        await asyncio.sleep(5)
        
        # Ferma scheduler
        stop_auto_analyzer()
        print("🛑 Scheduler fermato")
    else:
        print("[ERROR] Errore nell'avvio dello scheduler")

async def example_advanced_usage():
    """Esempio 2: Utilizzo avanzato con controllo diretto"""
    print("\n[INFO] Esempio 2: Utilizzo Avanzato")
    print("-" * 40)
    
    # Crea istanza diretta
    scheduler = AutoAnalyzeScheduler()
    
    # Avvia con configurazione personalizzata
    success = scheduler.start_auto_analyzer(user_id=2, interval_minutes=15)
    
    if success:
        print("[OK] Scheduler avanzato avviato")
        
        # Monitora per 10 secondi
        for i in range(10):
            status = scheduler.get_status()
            print(f"⏱️  {i+1}/10 - Status: {status['is_running']}")
            await asyncio.sleep(1)
        
        # Ferma
        scheduler.stop_scheduler()
        print("🛑 Scheduler avanzato fermato")
    else:
        print("[ERROR] Errore nell'avvio dello scheduler avanzato")

def example_multiple_users():
    """Esempio 3: Gestione di più utenti (simulato)"""
    print("\n[INFO] Esempio 3: Gestione Multi-Utente")
    print("-" * 40)
    
    users = [1, 2, 3]
    intervals = [60, 30, 15]  # minuti
    
    print("[INFO] Configurazione multi-utente:")
    for user_id, interval in zip(users, intervals):
        print(f"  - User {user_id}: ogni {interval} minuti")
    
    # Nota: Il sistema attuale supporta un solo utente per volta
    # Questo è un esempio di come potrebbe essere esteso
    print("\n[WARN]  Nota: Sistema attuale supporta un solo utente per volta")
    print("   Per supportare più utenti, il sistema dovrebbe essere esteso")

def example_integration_streamlit():
    """Esempio 4: Integrazione con Streamlit (codice di esempio)"""
    print("\n[INFO] Esempio 4: Integrazione Streamlit")
    print("-" * 40)
    
    streamlit_code = '''
import streamlit as st
from scheduler import start_auto_analyzer, stop_auto_analyzer, get_auto_analyzer_status

# Sidebar per controllo scheduler
with st.sidebar:
    st.header("[INFO] Auto-Analyze Scheduler")
    
    # Controlli
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Avvia Scheduler"):
            success = start_auto_analyzer(user_id=1, interval_minutes=60)
            if success:
                st.success("Scheduler avviato!")
            else:
                st.error("Errore nell'avvio")
    
    with col2:
        if st.button("⏹️ Ferma Scheduler"):
            stop_auto_analyzer()
            st.success("Scheduler fermato!")
    
    # Status
    status = get_auto_analyzer_status()
    st.json(status)
    
    # Configurazione
    st.subheader("[INFO] Configurazione")
    interval = st.slider("Intervallo (minuti)", 15, 360, 60)
    user_id = st.number_input("User ID", value=1, min_value=1)
    
    if st.button("[INFO] Riavvia con Nuova Config"):
        stop_auto_analyzer()
        success = start_auto_analyzer(user_id=user_id, interval_minutes=interval)
        if success:
            st.success(f"Scheduler riavviato per user {user_id} ogni {interval} minuti")
'''
    
    print("[INFO] Codice Streamlit di esempio:")
    print(streamlit_code)

def example_cli_usage():
    """Esempio 5: Utilizzo da riga di comando"""
    print("\n[INFO] Esempio 5: Utilizzo CLI")
    print("-" * 40)
    
    cli_examples = [
        "# Avvia scheduler per user_id=1 ogni 60 minuti (default)",
        "python scheduler/auto_scheduler.py --user-id 1",
        "",
        "# Avvia con intervallo personalizzato (15 minuti)",
        "python scheduler/auto_scheduler.py --user-id 1 --interval 15",
        "",
        "# Verifica status dello scheduler",
        "python scheduler/auto_scheduler.py --user-id 1 --status",
        "",
        "# Ferma lo scheduler",
        "python scheduler/auto_scheduler.py --user-id 1 --stop",
        "",
        "# Avvia per analisi intensiva (ogni 30 minuti)",
        "python scheduler/auto_scheduler.py --user-id 1 --interval 30",
        "",
        "# Avvia per server 24/7 (ogni 6 ore)",
        "python scheduler/auto_scheduler.py --user-id 1 --interval 360"
    ]
    
    print("💻 Comandi CLI di esempio:")
    for example in cli_examples:
        print(example)

def example_monitoring():
    """Esempio 6: Monitoraggio e logging"""
    print("\n[INFO] Esempio 6: Monitoraggio")
    print("-" * 40)
    
    monitoring_code = '''
# Monitoraggio continuo dello scheduler
import time
from scheduler import get_auto_analyzer_status

def monitor_scheduler():
    """Monitora lo scheduler e logga lo status"""
    while True:
        status = get_auto_analyzer_status()
        
        if status['is_running']:
            print(f"[OK] Scheduler attivo - User: {status['user_id']}, "
                  f"Intervallo: {status['interval_minutes']} min")
        else:
            print("⏸️  Scheduler inattivo")
        
        time.sleep(60)  # Controlla ogni minuto

# Avvia monitoraggio in background
import threading
monitor_thread = threading.Thread(target=monitor_scheduler, daemon=True)
monitor_thread.start()
'''
    
    print("[REPORT] Codice di monitoraggio:")
    print(monitoring_code)

async def main():
    """Funzione principale con tutti gli esempi"""
    print("[INFO] Esempi di Utilizzo - Auto-Analyze Scheduler")
    print("=" * 60)
    
    examples = [
        ("Utilizzo Base", example_basic_usage),
        ("Utilizzo Avanzato", example_advanced_usage),
        ("Multi-Utente", example_multiple_users),
        ("Integrazione Streamlit", example_integration_streamlit),
        ("Utilizzo CLI", example_cli_usage),
        ("Monitoraggio", example_monitoring),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        try:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
        except Exception as e:
            print(f"[ERROR] Errore nell'esempio {name}: {e}")
    
    print("\n" + "=" * 60)
    print("[INFO] Tutti gli esempi sono stati mostrati!")
    print("\n💡 Suggerimenti:")
    print("  - Usa intervalli di 15-30 minuti per test")
    print("  - Usa intervalli di 60+ minuti per produzione")
    print("  - Monitora sempre i log per errori")
    print("  - Integra con Streamlit per controllo web")

if __name__ == "__main__":
    asyncio.run(main()) 