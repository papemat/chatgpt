import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Configurazione API
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="TokIntel Cloud", layout="wide")

st.title("☁️ TokIntel Cloud Interface")

# Sidebar per selezione modalità
mode = st.sidebar.selectbox(
    "Modalità di Analisi",
    ["Analisi Video", "Analisi Testo", "Dashboard Analytics"]
)

if mode == "Analisi Video":
    st.header("🎥 Analisi Video")
    
    uploaded_file = st.file_uploader(
        "Carica un file video",
        type=['mp4', 'avi', 'mov', 'mkv']
    )
    
    if uploaded_file is not None:
        if st.button("Analizza Video"):
            with st.spinner("Analizzando il video..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(f"{API_BASE_URL}/analyze/video", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("[OK] Analisi completata!")
                        
                        # Mostra risultati
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("[RESULTS] Risultati Generali")
                            st.metric("Punteggio", f"{result['data'].get('overall_score', 0):.2f}")
                            st.metric("Potenziale Virale", f"{result['data'].get('viral_potential', 0):.2f}")
                            
                        with col2:
                            st.subheader("[TEAM] Analisi Team Devika")
                            if 'devika_analysis' in result['data']:
                                devika = result['data']['devika_analysis']
                                st.write(f"**Strategist:** {devika.get('overall_score', 0):.2f}")
                                st.write(f"**Copywriter:** {devika.get('viral_potential', 0):.2f}")
                        
                        # Mostra raccomandazioni
                        if 'devika_analysis' in result['data']:
                            st.subheader("[SUGGESTIONS] Raccomandazioni")
                            recommendations = result['data']['devika_analysis'].get('team_recommendations', [])
                            for i, rec in enumerate(recommendations[:5], 1):
                                st.write(f"{i}. {rec}")
                    else:
                        st.error(f"[ERROR] Errore: {response.text}")
                        
                except Exception as e:
                    st.error(f"[ERROR] Errore di connessione: {e}")

elif mode == "Analisi Testo":
    st.header("[INFO] Analisi Testo")
    
    text_content = st.text_area(
        "Inserisci il testo da analizzare",
        height=200,
        placeholder="Incolla qui il contenuto del video o il testo da analizzare..."
    )
    
    title = st.text_input("Titolo dell'analisi", "Analisi Testo")
    
    if st.button("Analizza Testo") and text_content:
        with st.spinner("Analizzando il testo..."):
            try:
                payload = {
                    "content": text_content,
                    "title": title
                }
                response = requests.post(f"{API_BASE_URL}/analyze/text", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("[OK] Analisi completata!")
                    
                    # Mostra risultati
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("[RESULTS] Risultati")
                        st.metric("Punteggio", f"{result['data'].get('overall_score', 0):.2f}")
                        st.metric("Engagement", f"{result['data'].get('engagement_prediction', 0):.2f}")
                    
                    with col2:
                        st.subheader("[ACTIONS] Azioni Prioritarie")
                        actions = result['data'].get('priority_actions', [])
                        for i, action in enumerate(actions[:3], 1):
                            st.write(f"{i}. {action}")
                    
                    # Mostra analisi degli agenti
                    st.subheader("[AGENTS] Analisi degli Agenti")
                    agents = result['data'].get('agent_analyses', [])
                    for agent in agents:
                        with st.expander(f"[AGENT] {agent['agent_name']}"):
                            st.write(f"**Confidenza:** {agent['confidence']:.2f}")
                            st.write(f"**Raccomandazioni:**")
                            for rec in agent['recommendations'][:3]:
                                st.write(f"• {rec}")
                                
                else:
                    st.error(f"[ERROR] Errore: {response.text}")
                    
            except Exception as e:
                st.error(f"[ERROR] Errore di connessione: {e}")

elif mode == "Dashboard Analytics":
    st.header("[REPORT] Dashboard Analytics")
    
    # Carica dati dall'API
    try:
        # Top videos
        response = requests.get(f"{API_BASE_URL}/analytics/top-videos")
        if response.status_code == 200:
            top_videos_data = response.json()['data']
            if top_videos_data:
                df_videos = pd.DataFrame(top_videos_data)
                st.subheader("🏆 Top Video")
                fig_videos = px.bar(
                    df_videos,
                    x='score',
                    y='title',
                    orientation='h',
                    title="Video con Punteggio Più Alto"
                )
                st.plotly_chart(fig_videos, use_container_width=True)
        
        # Sentiment trend
        response = requests.get(f"{API_BASE_URL}/analytics/sentiment-trend")
        if response.status_code == 200:
            sentiment_data = response.json()['data']
            if sentiment_data:
                df_sentiment = pd.DataFrame(sentiment_data)
                df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])
                st.subheader("[REPORT] Trend Sentiment")
                fig_sentiment = px.line(
                    df_sentiment,
                    x='date',
                    y='sentiment',
                    title="Evoluzione Sentiment"
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Keywords cloud
        response = requests.get(f"{API_BASE_URL}/analytics/keywords")
        if response.status_code == 200:
            keywords = response.json()['data']
            if keywords:
                st.subheader("☁️ Cloud Parole Chiave")
                text = ' '.join(keywords)
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
                
    except Exception as e:
        st.error(f"[ERROR] Errore nel caricamento dei dati: {e}")
        st.info("Assicurati che l'API sia in esecuzione su " + API_BASE_URL)

# Footer
st.markdown("---")
st.markdown("*TokIntel v2.1 Cloud Interface - Connesso a " + API_BASE_URL + "*") 