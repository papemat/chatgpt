import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analytics.dashboard import get_top_videos, get_sentiment_trend, get_keywords_cloud
import pandas as pd
from datetime import datetime
import json
import os

# Import Pro features
try:
    from utils.pdf_exporter import export_analysis_to_pdf
    from db.database import get_analysis_history, get_db_manager
    PRO_FEATURES_AVAILABLE = True
except ImportError:
    PRO_FEATURES_AVAILABLE = False
    st.warning("[WARN]️ Funzionalità Pro non disponibili. Installa requirements_pro.txt")

st.set_page_config(page_title="TokIntel Analytics", layout="wide")

st.title("[REPORT] TokIntel Analytics Dashboard")

# Sidebar per filtri e funzionalità Pro
st.sidebar.header("Filtri")
date_range = st.sidebar.date_input(
    "Intervallo date",
    value=(datetime.now().date(), datetime.now().date())
)

# Sezione Pro Features
if PRO_FEATURES_AVAILABLE:
    st.sidebar.markdown("---")
    st.sidebar.header("[READY] Funzionalità Pro")
    
    # Bottone per generare PDF
    if st.sidebar.button("[REPORT] Genera Report PDF"):
        try:
            # Crea dati di esempio per il report
            sample_data = {
                "video_title": "Analisi Dashboard TokIntel",
                "analysis_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "overall_score": avg_score if 'avg_score' in locals() else 75,
                "summary": "Report generato dalla dashboard analytics di TokIntel v2.1 Pro+",
                "key_points": [
                    f"Video analizzati: {len(top_videos) if top_videos else 0}",
                    f"Punteggio medio: {avg_score:.2f}" if 'avg_score' in locals() else "N/A",
                    f"Parole chiave uniche: {len(set(keywords)) if keywords else 0}",
                    "Dashboard generata automaticamente"
                ],
                "metrics": {
                    "engagement_rate": 4.2,
                    "completion_rate": 68,
                    "share_rate": 2.1,
                    "comment_rate": 1.8,
                    "like_rate": 3.5
                },
                "keywords": keywords if keywords else ["tiktok", "analisi", "dashboard"],
                "suggested_hashtags": ["#tokintel", "#analytics", "#tiktok", "#dashboard"],
                "recommendations": [
                    {
                        "title": "Continua l'Analisi",
                        "description": "Mantieni la frequenza di analisi per migliorare i risultati."
                    },
                    {
                        "title": "Monitora le Keywords",
                        "description": "Usa le parole chiave identificate per ottimizzare i contenuti."
                    }
                ],
                "duration": "Dashboard",
                "resolution": "Analytics",
                "format": "Report",
                "ai_model": "TokIntel v2.1",
                "version": "v2.1 Pro+"
            }
            
            pdf_path = export_analysis_to_pdf(sample_data)
            st.success(f"[OK] Report PDF generato: {pdf_path}")
            
            # Offri download
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="[INFO] Scarica Report PDF",
                    data=pdf_file.read(),
                    file_name=f"tokintel_analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            st.error(f"[ERROR] Errore nella generazione PDF: {e}")
    
    # Bottone per cronologia database
    if st.sidebar.button("[INFO] Cronologia Database"):
        try:
            history = get_analysis_history(limit=10)
            if history:
                st.sidebar.markdown("### [INFO] Ultime Analisi")
                for i, analysis in enumerate(history[:5], 1):
                    st.sidebar.markdown(f"**{i}.** {analysis['title'][:30]}...")
                    st.sidebar.markdown(f"Score: {analysis['score']} | {analysis['created_at'][:10]}")
            else:
                st.sidebar.info("Nessuna analisi nel database")
        except Exception as e:
            st.sidebar.error(f"Errore database: {e}")

# Sezione 1: Classifica video
st.header("🏆 Classifica Video")
top_videos = get_top_videos(limit=10)
if top_videos:
    df_videos = pd.DataFrame(top_videos, columns=['Titolo', 'Punteggio', 'Data'])
    df_videos['Data'] = pd.to_datetime(df_videos['Data'])
    
    fig_videos = px.bar(
        df_videos, 
        x='Punteggio', 
        y='Titolo',
        orientation='h',
        title="Top 10 Video per Punteggio"
    )
    st.plotly_chart(fig_videos, use_container_width=True)
else:
    st.info("Nessun video analizzato ancora.")

# Sezione 2: Trend Sentiment
st.header("[REPORT] Trend Sentiment")
sentiment_data = get_sentiment_trend()
if sentiment_data:
    df_sentiment = pd.DataFrame(sentiment_data, columns=['Data', 'Sentiment'])
    df_sentiment['Data'] = pd.to_datetime(df_sentiment['Data'])
    
    fig_sentiment = px.line(
        df_sentiment,
        x='Data',
        y='Sentiment',
        title="Evoluzione Sentiment nel Tempo"
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)
else:
    st.info("Dati sentiment non disponibili.")

# Sezione 3: Cloud Keywords
st.header("☁️ Cloud Parole Chiave")
keywords = get_keywords_cloud()
if keywords:
    # Crea wordcloud
    text = ' '.join(keywords)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.info("Nessuna parola chiave disponibile.")

# Sezione 4: Statistiche generali
st.header("[INFO] Statistiche Generali")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Video Analizzati", len(top_videos) if top_videos else 0)
with col2:
    avg_score = df_videos['Punteggio'].mean() if top_videos else 0
    st.metric("Punteggio Medio", f"{avg_score:.2f}")
with col3:
    st.metric("Parole Chiave Uniche", len(set(keywords)) if keywords else 0)
with col4:
    st.metric("Ultimo Aggiornamento", datetime.now().strftime("%H:%M"))

# Footer
st.markdown("---")
st.markdown("*Dashboard generata automaticamente da TokIntel v2.1*") 