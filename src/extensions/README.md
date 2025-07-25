# 📤 TokIntel Export Tools

Modulo di utility per esportazione avanzata dei dati TokIntel in multipli formati.

## 🎯 Funzionalità

- **CSV Export** - Per analisi dati e fogli di calcolo
- **PDF Export** - Per report stampabili e condivisibili
- **Excel Export** - Per analisi avanzate con formattazione
- **ZIP Export** - Pacchetto completo con tutti i formati
- **Bundle Export** - Esportazione completa con timestamp

## 📦 Installazione

```bash
pip install reportlab openpyxl
```

## 🚀 Utilizzo Rapido

```python
from export_tools import export_to_csv, export_to_pdf, export_to_excel, export_to_zip

# Dati di esempio
dati_csv = [
    {"Video": "TikTok1", "Autore": "User123", "Score": 8.5},
    {"Video": "TikTok2", "Autore": "User456", "Score": 6.2}
]

dati_pdf = {
    "Analisi": "TikTok1",
    "Punteggio": "85/100",
    "Raccomandazioni": "Continuare con contenuti simili"
}

# Esporta in diversi formati
export_to_csv(dati_csv, "risultati.csv")
export_to_pdf(dati_pdf, "report.pdf")
export_to_excel(dati_csv, "analisi.xlsx")

# Esporta tutto in ZIP
zip_data = {'csv_data': dati_csv, 'json_data': dati_pdf}
zip_path = export_to_zip(zip_data, "exports/")
```

## 📋 API Reference

### `export_to_csv(data, filepath)`
Esporta una lista di dizionari in formato CSV.

**Parametri:**
- `data` (List[dict]): Lista di dizionari da esportare
- `filepath` (str): Percorso del file CSV di output

**Esempio:**
```python
dati = [{"Nome": "Alice", "Età": 30}, {"Nome": "Bob", "Età": 25}]
export_to_csv(dati, "utenti.csv")
```

### `export_to_pdf(data, filepath)`
Esporta un dizionario in formato PDF.

**Parametri:**
- `data` (dict): Dizionario da esportare
- `filepath` (str): Percorso del file PDF di output

**Esempio:**
```python
report = {"Titolo": "Analisi", "Risultato": "Positivo"}
export_to_pdf(report, "analisi.pdf")
```

### `export_to_excel(data, filepath)`
Esporta una lista di dizionari in formato Excel (.xlsx).

**Parametri:**
- `data` (List[dict]): Lista di dizionari da esportare
- `filepath` (str): Percorso del file Excel di output

**Caratteristiche:**
- Header colorati (blu)
- Auto-adjust colonne
- Formattazione professionale

### `export_to_zip(data, output_dir)`
Crea un file ZIP con tutti i dati in multipli formati.

**Parametri:**
- `data` (dict): Dizionario con 'csv_data' e 'json_data'
- `output_dir` (str): Directory di output

**Contenuto ZIP:**
- `export.csv` - Dati in formato CSV
- `export.json` - Dati in formato JSON
- `metadata.json` - Metadati dell'esportazione
- `README.txt` - Documentazione del contenuto

### `export_bundle(data, output_dir)`
Esporta un bundle completo con tutti i formati disponibili.

**Parametri:**
- `data` (dict): Dizionario con 'csv_data' e 'json_data'
- `output_dir` (str): Directory di output

**Output:**
- Crea una cartella con tutti i file
- Genera un ZIP finale con tutto il contenuto

## 🧪 Test

Esegui i test automatici:

```bash
python -m pytest test_export_tools.py -v
```

**Risultato atteso:**
```
9 passed in 0.26s
```

## 📊 Esempio Completo

Vedi `example_usage.py` per un esempio completo di tutte le funzionalità.

```bash
python example_usage.py
```

## 🔧 Integrazione UI

Per integrare nella UI Streamlit:

```python
import streamlit as st
from export_tools import export_to_csv, export_to_pdf, export_to_excel, export_to_zip

# Bottoni di esportazione
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📄 Esporta CSV"):
        export_to_csv(dati_csv, "export.csv")
        st.success("✅ CSV generato!")

with col2:
    if st.button("🧾 Esporta PDF"):
        export_to_pdf(dati_pdf, "export.pdf")
        st.success("✅ PDF generato!")

with col3:
    if st.button("📊 Esporta Excel"):
        export_to_excel(dati_csv, "export.xlsx")
        st.success("✅ Excel generato!")

with col4:
    if st.button("📦 Esporta ZIP"):
        zip_path = export_to_zip(zip_data, ".")
        st.success("✅ ZIP generato!")
```

## 🐛 Gestione Errori

Il modulo gestisce automaticamente:

- **Dati vuoti**: Solleva `ValueError` con messaggio chiaro
- **Dipendenze mancanti**: Solleva `ImportError` con istruzioni
- **Percorsi non validi**: Crea automaticamente le directory necessarie
- **File esistenti**: Sovrascrive senza warning

## 📈 Prossimi Sviluppi

- [ ] Supporto per più fogli Excel
- [ ] Template PDF personalizzabili
- [ ] Compressione ZIP avanzata
- [ ] Export asincrono per file grandi
- [ ] Integrazione con database

## 📝 Changelog

### v2.1.0 (2025-07-25)
- ✅ Aggiunto supporto Excel con formattazione
- ✅ Aggiunto export ZIP con metadati
- ✅ Aggiunta funzione export_bundle
- ✅ Test completi (9 test passati)
- ✅ Documentazione completa

### v2.0.0 (2025-07-24)
- ✅ Funzioni base CSV e PDF
- ✅ Gestione errori
- ✅ Test unitari

---

**Autore:** Matteo Papetti  
**Progetto:** TokIntel v2 Extensions  
**Versione:** 2.1.0 