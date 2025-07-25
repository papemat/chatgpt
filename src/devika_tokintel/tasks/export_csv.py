import os
import sys
import csv
import json
from datetime import datetime

def run():
    print("[REPORT] Exporting TokIntel data to CSV...")
    
    # Aggiungi il path di TokIntel
    tokintel_path = os.path.join(os.path.dirname(__file__), "..", "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    output_dir = os.path.join(tokintel_path, "output")
    export_dir = os.path.join(os.path.dirname(__file__), "exports")
    
    # Crea directory export se non esiste
    os.makedirs(export_dir, exist_ok=True)
    
    exports_created = []
    
    try:
        # Esporta file di output
        if os.path.exists(output_dir):
            print(f"[INFO] Scanning output directory: {output_dir}")
            
            for filename in os.listdir(output_dir):
                if filename.endswith('.json'):
                    json_path = os.path.join(output_dir, filename)
                    csv_filename = filename.replace('.json', '.csv')
                    csv_path = os.path.join(export_dir, csv_filename)
                    
                    try:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Converti JSON a CSV
                        if isinstance(data, list) and len(data) > 0:
                            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                                if data:
                                    fieldnames = data[0].keys()
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerows(data)
                                    
                                    exports_created.append(csv_filename)
                                    print(f"  [OK] Exported {filename} → {csv_filename}")
                        
                        elif isinstance(data, dict):
                            # Per dati singoli, crea una riga
                            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                                fieldnames = data.keys()
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerow(data)
                                
                                exports_created.append(csv_filename)
                                print(f"  [OK] Exported {filename} → {csv_filename}")
                    
                    except Exception as e:
                        print(f"  [ERROR] Failed to export {filename}: {e}")
        
        # Esporta configurazione
        config_path = os.path.join(tokintel_path, "config.yaml")
        if os.path.exists(config_path):
            try:
                import yaml
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Flatten config per CSV
                flat_config = flatten_dict(config)
                
                config_csv_path = os.path.join(export_dir, "config_export.csv")
                with open(config_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['key', 'value']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for key, value in flat_config.items():
                        writer.writerow({'key': key, 'value': str(value)})
                
                exports_created.append("config_export.csv")
                print(f"  [OK] Exported config.yaml → config_export.csv")
                
            except Exception as e:
                print(f"  [ERROR] Failed to export config: {e}")
        
        # Crea report di export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(export_dir, f"export_report_{timestamp}.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"Devika Export Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Files exported: {len(exports_created)}\n")
            for filename in exports_created:
                f.write(f"  - {filename}\n")
            f.write(f"\nExport directory: {export_dir}\n")
        
        print(f"\n[INFO] Export Summary:")
        print(f"  Files exported: {len(exports_created)}")
        print(f"  Export directory: {export_dir}")
        print(f"  Report created: export_report_{timestamp}.txt")
        
        if exports_created:
            print("[INFO] Export completed successfully!")
        else:
            print("[WARN]️ No files were exported")
            
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dictionary for CSV export"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items) 