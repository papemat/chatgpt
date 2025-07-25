"""
Esempio di Task Personalizzato per Devika
=========================================

Questo file mostra come creare un task personalizzato per Devika.
Copia questo file, modifica il nome e la logica, poi registralo in task_runner.py
"""

import os
import sys
import yaml
from datetime import datetime

def run():
    """
    Funzione principale del task.
    Questa funzione viene chiamata quando esegui: python devika.py nome_task
    """
    print("[INFO] Eseguendo task personalizzato...")
    
    # 1. Aggiungi il path di TokIntel
    tokintel_path = os.path.join(os.path.dirname(__file__), "..", "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    # 2. Carica configurazione Devika (opzionale)
    devika_config_path = os.path.join(os.path.dirname(__file__), "..", "devika_config.yaml")
    if os.path.exists(devika_config_path):
        try:
            with open(devika_config_path, 'r') as f:
                devika_config = yaml.safe_load(f)
            print("[OK] Configurazione Devika caricata")
        except Exception as e:
            print(f"[WARN]️ Errore caricamento config Devika: {e}")
    
    # 3. La tua logica personalizzata qui
    print("[INFO] Eseguendo logica personalizzata...")
    
    # Esempio: conta i file Python in TokIntel
    python_files = []
    for root, dirs, files in os.walk(tokintel_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"[INFO] Trovati {len(python_files)} file Python in TokIntel")
    
    # Esempio: verifica dimensione directory
    total_size = 0
    for file_path in python_files:
        try:
            total_size += os.path.getsize(file_path)
        except:
            pass
    
    print(f"💾 Dimensione totale: {total_size / 1024:.1f} KB")
    
    # 4. Salva risultati (opzionale)
    results = {
        'timestamp': datetime.now().isoformat(),
        'python_files_count': len(python_files),
        'total_size_kb': total_size / 1024,
        'files': [os.path.basename(f) for f in python_files[:10]]  # Primi 10 file
    }
    
    # Salva in reports/
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"custom_task_report_{timestamp}.json")
    
    import json
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"[INFO] Report salvato: {report_path}")
    print("[OK] Task personalizzato completato!")

def get_task_info():
    """
    Informazioni sul task (opzionale)
    """
    return {
        'name': 'Custom Task Example',
        'description': 'Esempio di task personalizzato',
        'version': '1.0',
        'author': 'Your Name',
        'category': 'analysis'
    }

# Per testare il task direttamente
if __name__ == "__main__":
    run() 