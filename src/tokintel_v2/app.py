import streamlit as st
import time

st.set_page_config(page_title="TokIntel HuggingFace Demo", layout="centered")
st.title("\U0001F916 TokIntel v2 Demo (HuggingFace Spaces)")

st.write("""
Questa è una demo pubblica di TokIntel v2 su HuggingFace Spaces.\n
Carica un video, avvia l'analisi e visualizza i risultati mockati (OCR, trascrizione AI, metadati).\n
*Nota: questa versione non esegue analisi reali, ma mostra il flusso e l'interfaccia.*
""")

uploaded_file = st.file_uploader("Carica un file video", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    if st.button("Analizza Video"):
        with st.spinner("Analisi in corso..."):
            time.sleep(2)  # Simula tempo di analisi
            # Output mock realistici
            ocr_text = "Testo OCR rilevato: 'Benvenuti su TokIntel!'"
            ai_transcription = "Nel video si parla di strategie di marketing su TikTok."
            metadata = {
                "Durata stimata": "00:42",
                "Topic stimato": "Marketing, Social Media",
                "Risoluzione": "1920x1080"
            }
        st.success("Analisi completata!")
        st.subheader("\U0001F4DD Testo OCR")
        st.write(ocr_text)
        st.subheader("\U0001F916 Trascrizione AI")
        st.write(ai_transcription)
        st.subheader("\U0001F4C8 Metadati Video")
        for k, v in metadata.items():
            st.write(f"**{k}:** {v}")

# ---
# Questa demo è pronta per HuggingFace Spaces. Adatta le funzioni reali sostituendo i mock dove necessario. 