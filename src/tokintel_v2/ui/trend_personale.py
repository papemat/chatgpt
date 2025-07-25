#!/usr/bin/env python3
"""
[REPORT] Trend Personale - TokIntel v2
Interfaccia per visualizzare i trend personali dell'utente
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
from pathlib import Path

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from analytics.trend_analyzer import get_trend_analyzer, analyze_user_trends
from db.database import get_db_manager
from core.logger import setup_logger

logger = setup_logger(__name__)

class TrendPersonaleDashboard:
    """Dashboard per i trend personali dell'utente"""
    
    def __init__(self):
        """Inizializza la dashboard"""
        self.db_manager = get_db_manager()
        self.trend_analyzer = get_trend_analyzer()
        
    def setup_page(self):
        """Configura la pagina Streamlit"""
        st.set_page_config(
            page_title="Trend Personale - TokIntel v2",
            page_icon="[REPORT]",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .trend-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .insight-badge {
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            margin: 0.25rem;
            display: inline-block;
        }
        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="trend-header"><h1>[REPORT] I Tuoi Trend Personali</h1><p>Scopri i pattern nei tuoi contenuti TikTok</p></div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Rende la sidebar con filtri"""
        with st.sidebar:
            st.header("[INFO] Filtri")
            
            # Periodo di analisi
            st.subheader("📅 Periodo di Analisi")
            period_days = st.selectbox(
                "Analizza gli ultimi:",
                [7, 30, 90, 180, 365],
                index=1,  # Default 30 giorni
                format_func=lambda x: f"{x} giorni"
            )
            
            # Utente (per ora fisso a 1, in futuro dinamico)
            user_id = st.number_input("ID Utente", value=1, min_value=1, step=1)
            
            st.divider()
            
            # Statistiche rapide
            st.subheader("[REPORT] Statistiche Rapide")
            try:
                insights = self.trend_analyzer.get_user_insights(user_id, period_days)
                summary = insights.get('summary', {})
                
                st.metric(
                    "Video Analizzati",
                    summary.get('total_analyzed_videos', 0)
                )
                
                if summary.get('top_keyword') != 'N/A':
                    st.metric(
                        "Keyword Top",
                        f"{summary['top_keyword']} ({summary['top_keyword_count']})"
                    )
                
                if summary.get('top_emotion') != 'N/A':
                    st.metric(
                        "Emozione Top",
                        f"{summary['top_emotion']} ({summary['top_emotion_count']})"
                    )
                    
            except Exception as e:
                st.error(f"Errore nel caricamento statistiche: {e}")
            
            return user_id, period_days
    
    def render_keywords_chart(self, keywords: Dict[str, int]):
        """Rende il grafico delle parole chiave"""
        if not keywords:
            st.info("Nessuna parola chiave trovata per questo periodo.")
            return
        
        # Prepara dati per il grafico
        df = pd.DataFrame(list(keywords.items()), columns=['Keyword', 'Frequenza'])
        df = df.sort_values('Frequenza', ascending=True)
        
        # Crea grafico a barre orizzontali
        fig = px.bar(
            df,
            x='Frequenza',
            y='Keyword',
            orientation='h',
            title="[INFO] Parole Chiave Più Utilizzate",
            color='Frequenza',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Frequenza",
            yaxis_title="Parole Chiave"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_emotions_chart(self, emotions: Dict[str, int]):
        """Rende il grafico delle emozioni"""
        if not emotions:
            st.info("Nessuna emozione identificata per questo periodo.")
            return
        
        # Prepara dati per il grafico
        df = pd.DataFrame(list(emotions.items()), columns=['Emozione', 'Frequenza'])
        
        # Crea grafico a torta
        fig = px.pie(
            df,
            values='Frequenza',
            names='Emozione',
            title="😊 Distribuzione Emozioni",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_trend_timeline(self, trends_data: List[Dict[str, Any]]):
        """Rende la timeline dei trend"""
        if not trends_data:
            st.info("Nessun dato di trend disponibile per questo periodo.")
            return
        
        # Converti in DataFrame
        df = pd.DataFrame(trends_data)
        
        if df.empty:
            st.info("Nessun dato di trend disponibile.")
            return
        
        # Filtra solo i dati di score per la timeline
        score_df = df[df['type'] == 'score'].copy()
        
        if score_df.empty:
            st.info("Nessun dato di performance disponibile per la timeline.")
            return
        
        # Converti date
        score_df['date'] = pd.to_datetime(score_df['date'])
        score_df = score_df.sort_values('date')
        
        # Crea grafico timeline
        fig = px.line(
            score_df,
            x='date',
            y='value',
            title="[REPORT] Trend Performance nel Tempo",
            labels={'value': 'Score', 'date': 'Data'}
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Data",
            yaxis_title="Score Performance"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_content_themes(self, user_id: int, days: int):
        """Rende i temi del contenuto"""
        try:
            themes = self.trend_analyzer.get_content_themes(user_id, days)
            
            if not themes:
                st.info("Nessun tema identificato per questo periodo.")
                return
            
            st.subheader("🎯 Temi del Contenuto")
            
            for i, theme in enumerate(themes[:5]):  # Top 5 temi
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{theme['theme'].title()}**")
                        if theme['keywords']:
                            keywords_text = ", ".join(theme['keywords'][:5])  # Top 5 keywords
                            st.caption(f"Keywords: {keywords_text}")
                    
                    with col2:
                        st.metric("Score", theme['score'])
                
                if i < len(themes) - 1:
                    st.divider()
                    
        except Exception as e:
            st.error(f"Errore nel caricamento temi: {e}")
    
    def render_insights_summary(self, insights: Dict[str, Any]):
        """Rende il riepilogo degli insights"""
        summary = insights.get('summary', {})
        
        st.subheader("💡 Insights Principali")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Video Analizzati",
                summary.get('total_analyzed_videos', 0),
                help="Numero totale di video analizzati nel periodo"
            )
        
        with col2:
            top_keyword = summary.get('top_keyword', 'N/A')
            if top_keyword != 'N/A':
                st.metric(
                    "Keyword Top",
                    top_keyword,
                    delta=f"+{summary.get('top_keyword_count', 0)}",
                    help="Parola chiave più utilizzata"
                )
            else:
                st.metric("Keyword Top", "N/A")
        
        with col3:
            top_emotion = summary.get('top_emotion', 'N/A')
            if top_emotion != 'N/A':
                st.metric(
                    "Emozione Top",
                    top_emotion,
                    delta=f"+{summary.get('top_emotion_count', 0)}",
                    help="Emozione più frequente"
                )
            else:
                st.metric("Emozione Top", "N/A")
        
        with col4:
            st.metric(
                "Periodo Analisi",
                f"{summary.get('analysis_period_days', 0)} giorni",
                help="Periodo di analisi selezionato"
            )
    
    def render_export_options(self, insights: Dict[str, Any]):
        """Rende le opzioni di esportazione"""
        st.subheader("[INFO] Esporta Dati")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("[INFO] Esporta come JSON"):
                try:
                    json_str = json.dumps(insights, indent=2, default=str)
                    st.download_button(
                        label="⬇️ Scarica JSON",
                        data=json_str,
                        file_name=f"trend_personale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Errore nell'esportazione JSON: {e}")
        
        with col2:
            if st.button("[REPORT] Esporta come CSV"):
                try:
                    # Crea DataFrame per keywords
                    keywords_df = pd.DataFrame(list(insights.get('keywords', {}).items()), 
                                             columns=['Keyword', 'Frequenza'])
                    
                    # Crea DataFrame per emozioni
                    emotions_df = pd.DataFrame(list(insights.get('emotions', {}).items()), 
                                             columns=['Emozione', 'Frequenza'])
                    
                    # Combina in un unico CSV
                    combined_data = []
                    for keyword, freq in insights.get('keywords', {}).items():
                        combined_data.append({'Tipo': 'Keyword', 'Valore': keyword, 'Frequenza': freq})
                    
                    for emotion, freq in insights.get('emotions', {}).items():
                        combined_data.append({'Tipo': 'Emozione', 'Valore': emotion, 'Frequenza': freq})
                    
                    combined_df = pd.DataFrame(combined_data)
                    
                    csv_str = combined_df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Scarica CSV",
                        data=csv_str,
                        file_name=f"trend_personale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Errore nell'esportazione CSV: {e}")
    
    def run(self):
        """Esegue la dashboard"""
        try:
            # Setup pagina
            self.setup_page()
            
            # Sidebar
            user_id, period_days = self.render_sidebar()
            
            # Contenuto principale
            try:
                # Carica insights
                insights = self.trend_analyzer.get_user_insights(user_id, period_days)
                
                # Riepilogo insights
                self.render_insights_summary(insights)
                
                # Grafici
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("[INFO] Parole Chiave")
                    self.render_keywords_chart(insights.get('keywords', {}))
                
                with col2:
                    st.subheader("😊 Emozioni")
                    self.render_emotions_chart(insights.get('emotions', {}))
                
                # Timeline trend
                st.subheader("[REPORT] Timeline Performance")
                self.render_trend_timeline(insights.get('trends', []))
                
                # Temi del contenuto
                self.render_content_themes(user_id, period_days)
                
                # Opzioni di esportazione
                self.render_export_options(insights)
                
            except Exception as e:
                st.error(f"Errore nel caricamento dei dati: {e}")
                logger.error(f"Errore dashboard trend: {e}")
                
        except Exception as e:
            st.error(f"Errore nell'inizializzazione della dashboard: {e}")
            logger.error(f"Errore inizializzazione dashboard trend: {e}")

def main():
    """Funzione principale"""
    dashboard = TrendPersonaleDashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 