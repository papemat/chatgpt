#!/usr/bin/env python3
"""
Esempio di utilizzo del modulo export_tools.py
Dimostra tutte le funzionalità di esportazione: CSV, PDF, Excel, ZIP
"""

from export_tools import export_to_csv, export_to_pdf, export_to_excel, export_to_zip, export_bundle

def main():
    """Esempio completo di utilizzo del modulo export_tools"""
    
    print("=" * 60)
    print("TokIntel Export Tools - Esempio di Utilizzo")
    print("=" * 60)
    
    # Dati di esempio
    dati_csv = [
        {"Video": "TikTok1", "Autore": "User123", "Sentiment": "Positivo", "Score": 8.5},
        {"Video": "TikTok2", "Autore": "User456", "Sentiment": "Neutro", "Score": 6.2},
        {"Video": "TikTok3", "Autore": "User789", "Sentiment": "Positivo", "Score": 9.1},
        {"Video": "TikTok4", "Autore": "UserABC", "Sentiment": "Negativo", "Score": 3.8}
    ]
    
    dati_pdf = {
        "Analisi": "TikTok1",
        "Contenuto": "Tratta di IA e tool utili per la produttività",
        "Sentiment": "Positivo",
        "Tags": "AI, productivity, tools",
        "Punteggio": "85/100",
        "Raccomandazioni": "Continuare con contenuti simili",
        "Data_Analisi": "2024-01-15"
    }
    
    print("\n📊 Dati di esempio:")
    print(f"  - {len(dati_csv)} righe CSV")
    print(f"  - {len(dati_pdf)} campi PDF")
    
    try:
        # 1. Esporta CSV
        print("\n📄 Esportazione CSV...")
        export_to_csv(dati_csv, "esempio_export.csv")
        print("  ✅ CSV creato: esempio_export.csv")
        
        # 2. Esporta PDF
        print("\n🧾 Esportazione PDF...")
        export_to_pdf(dati_pdf, "esempio_export.pdf")
        print("  ✅ PDF creato: esempio_export.pdf")
        
        # 3. Esporta Excel
        print("\n📊 Esportazione Excel...")
        export_to_excel(dati_csv, "esempio_export.xlsx")
        print("  ✅ Excel creato: esempio_export.xlsx")
        
        # 4. Esporta ZIP
        print("\n📦 Esportazione ZIP...")
        zip_data = {
            'csv_data': dati_csv,
            'json_data': dati_pdf
        }
        zip_path = export_to_zip(zip_data, ".")
        print(f"  ✅ ZIP creato: {zip_path}")
        
        # 5. Esporta Bundle completo
        print("\n🎁 Esportazione Bundle completo...")
        bundle_path = export_bundle(zip_data, ".")
        print(f"  ✅ Bundle creato: {bundle_path}")
        
        print("\n" + "=" * 60)
        print("✅ TUTTE LE ESPORTAZIONI COMPLETATE CON SUCCESSO!")
        print("=" * 60)
        
        print("\n📁 File creati:")
        import os
        for file in os.listdir("."):
            if file.startswith("esempio_export") or file.startswith("tokintel_export") or file.startswith("tokintel_bundle"):
                size = os.path.getsize(file)
                print(f"  - {file} ({size} bytes)")
        
        print("\n🎯 Prossimi step:")
        print("  1. Apri i file per verificare il contenuto")
        print("  2. Integra le funzioni nella UI Streamlit")
        print("  3. Personalizza i formati per le tue esigenze")
        
    except Exception as e:
        print(f"\n❌ Errore durante l'esportazione: {e}")
        print("Verifica che tutte le dipendenze siano installate:")
        print("  pip install reportlab openpyxl")

if __name__ == "__main__":
    main() 