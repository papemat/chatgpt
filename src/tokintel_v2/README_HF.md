# TokIntel v2 - Demo HuggingFace Spaces

Questa demo mostra il flusso base di TokIntel v2 su HuggingFace Spaces con output mockati (OCR, trascrizione AI, metadati).

## Come provarla

1. Carica la cartella TokIntel_v2 su HuggingFace Spaces (modalità Streamlit)
2. Assicurati che `app.py` e `requirements_hf.txt` siano nella root
3. Su HuggingFace Spaces, imposta come file principale `app.py` e requirements `requirements_hf.txt`
4. Avvia la Space: la demo sarà subito navigabile da browser

## Cosa fa la demo?
- Permette upload di un video
- Simula analisi (OCR, trascrizione AI, parsing metadati) con output realistici mock
- Mostra l'interfaccia e il flusso TokIntel v2

## Limiti
- Nessuna analisi reale: tutti gli output sono mockati
- Nessuna dipendenza non supportata su HuggingFace Spaces (no ffmpeg, no API esterne, no Ollama)

## Adattamenti futuri
- Sostituisci i mock con funzioni reali quando compatibili
- Aggiorna requirements se aggiungi moduli supportati

---
Demo pronta per pubblico e stakeholder! [INFO] 