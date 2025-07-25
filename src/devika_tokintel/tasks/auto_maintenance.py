import os
import sys
import shutil
import glob
from datetime import datetime, timedelta

def run():
    print("[INFO] Eseguendo manutenzione automatica...")
    
    # Aggiungi il path di TokIntel
    tokintel_path = os.path.join(os.path.dirname(__file__), "..", "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    maintenance_report = {
        'timestamp': datetime.now().isoformat(),
        'actions': [],
        'files_cleaned': 0,
        'space_freed': 0
    }
    
    # 1. Pulizia log vecchi
    print("🧹 Pulizia log vecchi...")
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    if os.path.exists(logs_dir):
        old_logs = []
        for log_file in glob.glob(os.path.join(logs_dir, "*.log")):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(log_file))
            if file_age.days > 7:  # Log più vecchi di 7 giorni
                old_logs.append(log_file)
        
        for log_file in old_logs:
            try:
                file_size = os.path.getsize(log_file)
                os.remove(log_file)
                maintenance_report['files_cleaned'] += 1
                maintenance_report['space_freed'] += file_size
                print(f"  [OK] Rimosso: {os.path.basename(log_file)}")
                maintenance_report['actions'].append(f"Rimosso log vecchio: {os.path.basename(log_file)}")
            except Exception as e:
                print(f"  [ERROR] Errore rimozione {log_file}: {e}")
    
    # 2. Pulizia report vecchi
    print("[INFO] Pulizia report vecchi...")
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if os.path.exists(reports_dir):
        old_reports = []
        for report_file in glob.glob(os.path.join(reports_dir, "*.json")):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(report_file))
            if file_age.days > 30:  # Report più vecchi di 30 giorni
                old_reports.append(report_file)
        
        for report_file in old_reports:
            try:
                file_size = os.path.getsize(report_file)
                os.remove(report_file)
                maintenance_report['files_cleaned'] += 1
                maintenance_report['space_freed'] += file_size
                print(f"  [OK] Rimosso: {os.path.basename(report_file)}")
                maintenance_report['actions'].append(f"Rimosso report vecchio: {os.path.basename(report_file)}")
            except Exception as e:
                print(f"  [ERROR] Errore rimozione {report_file}: {e}")
    
    # 3. Pulizia export temporanei
    print("[REPORT] Pulizia export temporanei...")
    exports_dir = os.path.join(os.path.dirname(__file__), "exports")
    if os.path.exists(exports_dir):
        temp_exports = []
        for export_file in glob.glob(os.path.join(exports_dir, "temp_*.csv")):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(export_file))
            if file_age.days > 1:  # Export temporanei più vecchi di 1 giorno
                temp_exports.append(export_file)
        
        for export_file in temp_exports:
            try:
                file_size = os.path.getsize(export_file)
                os.remove(export_file)
                maintenance_report['files_cleaned'] += 1
                maintenance_report['space_freed'] += file_size
                print(f"  [OK] Rimosso: {os.path.basename(export_file)}")
                maintenance_report['actions'].append(f"Rimosso export temporaneo: {os.path.basename(export_file)}")
            except Exception as e:
                print(f"  [ERROR] Errore rimozione {export_file}: {e}")
    
    # 4. Verifica integrità TokIntel
    print("[INFO] Verifica integrità TokIntel...")
    required_files = [
        os.path.join(tokintel_path, "config.yaml"),
        os.path.join(tokintel_path, "main.py"),
        os.path.join(tokintel_path, "requirements.txt")
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(os.path.basename(file_path))
    
    if missing_files:
        print(f"  [WARN]️ File mancanti: {', '.join(missing_files)}")
        maintenance_report['actions'].append(f"File mancanti rilevati: {', '.join(missing_files)}")
    else:
        print("  [OK] Tutti i file essenziali presenti")
        maintenance_report['actions'].append("Integrità file verificata")
    
    # 5. Ottimizzazione cache
    print("⚡ Ottimizzazione cache...")
    cache_dirs = [
        os.path.join(tokintel_path, "__pycache__"),
        os.path.join(tokintel_path, "*.pyc")
    ]
    
    cache_cleaned = 0
    for cache_pattern in cache_dirs:
        if os.path.isdir(cache_pattern):
            try:
                shutil.rmtree(cache_pattern)
                cache_cleaned += 1
                print(f"  [OK] Cache rimossa: {cache_pattern}")
                maintenance_report['actions'].append(f"Cache rimossa: {cache_pattern}")
            except Exception as e:
                print(f"  [ERROR] Errore rimozione cache {cache_pattern}: {e}")
    
    # 6. Backup configurazione
    print("💾 Backup configurazione...")
    config_path = os.path.join(tokintel_path, "config.yaml")
    if os.path.exists(config_path):
        backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"config_backup_{timestamp}.yaml")
        
        try:
            shutil.copy2(config_path, backup_path)
            print(f"  [OK] Backup creato: {os.path.basename(backup_path)}")
            maintenance_report['actions'].append(f"Backup config creato: {os.path.basename(backup_path)}")
        except Exception as e:
            print(f"  [ERROR] Errore backup: {e}")
    
    # Summary
    print(f"\n[REPORT] Report Manutenzione:")
    print(f"  File puliti: {maintenance_report['files_cleaned']}")
    print(f"  Spazio liberato: {maintenance_report['space_freed'] / 1024:.1f} KB")
    print(f"  Azioni eseguite: {len(maintenance_report['actions'])}")
    
    if maintenance_report['actions']:
        print(f"\n[INFO] Azioni eseguite:")
        for action in maintenance_report['actions']:
            print(f"  - {action}")
    
    # Salva report manutenzione
    maintenance_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(maintenance_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(maintenance_dir, f"maintenance_report_{timestamp}.json")
    
    import json
    with open(report_path, 'w') as f:
        json.dump(maintenance_report, f, indent=2)
    
    print(f"\n[INFO] Report manutenzione salvato: {report_path}")
    print("[INFO] Manutenzione completata!")
    
    return maintenance_report 