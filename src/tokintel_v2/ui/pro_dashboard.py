"""
[INFO] Dashboard Pro Avanzata - TokIntel v2.1
Dashboard completa che integra tutte le funzionalità Pro
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Import Pro features
try:
    from utils.pdf_exporter import export_analysis_to_pdf, create_sample_report
    from db.database import get_analysis_history, get_db_manager, init_database
    from ui.chat_agents import AgentChat
    PRO_FEATURES_AVAILABLE = True
except ImportError:
    PRO_FEATURES_AVAILABLE = False
    st.error("[ERRORE] Funzionalità Pro non disponibili. Installa requirements_pro.txt")

def init_session_state():
    """Inizializza lo stato della sessione"""
    if 'pro_dashboard_initialized' not in st.session_state:
        st.session_state.pro_dashboard_initialized = True
        st.session_state.selected_agent = "strategist"
        st.session_state.chat_messages = []
        st.session_state.current_analysis = None

def render_header():
    """Rende l'header della dashboard"""
    st.set_page_config(
        page_title="TokIntel Pro Dashboard",
        page_icon="[READY]",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("[READY] TokIntel v2.1 Pro+ Dashboard")
        st.markdown("**Dashboard completa con AI Agents, Analytics e Reportistica**")
    
    with col2:
        st.metric("Versione", "v2.1 Pro+")
    
    with col3:
        if PRO_FEATURES_AVAILABLE:
            st.success("[OK] Pro Active")
        else:
            st.error("[ERROR] Pro Inactive")

def render_sidebar():
    """Rende la sidebar con controlli"""
    st.sidebar.header("🎛️ Controlli Pro")
    
    # Sezione Database
    st.sidebar.subheader("💾 Database")
    if st.sidebar.button("🗄️ Inizializza DB"):
        try:
            init_database("sqlite:///tokintel_pro.db")
            st.sidebar.success("Database inizializzato!")
        except Exception as e:
            st.sidebar.error(f"Errore: {e}")
    
    # Sezione Chat
    st.sidebar.subheader("💬 Chat Agents")
    agent_options = ["strategist", "copywriter", "analyst"]
    selected_agent = st.sidebar.selectbox(
        "Seleziona Agente",
        agent_options,
        index=agent_options.index(st.session_state.selected_agent)
    )
    st.session_state.selected_agent = selected_agent
    
    # Sezione Report
    st.sidebar.subheader("[REPORT] Report")
    if st.sidebar.button("[REPORT] Genera Report PDF"):
        try:
            pdf_path = create_sample_report()
            st.sidebar.success(f"Report generato: {pdf_path}")
            
            # Download button
            with open(pdf_path, "rb") as pdf_file:
                st.sidebar.download_button(
                    label="[INFO] Scarica PDF",
                    data=pdf_file.read(),
                    file_name=f"tokintel_pro_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.sidebar.error(f"Errore: {e}")
    
    # Sezione Analytics
    st.sidebar.subheader("[REPORT] Analytics")
    if st.sidebar.button("[INFO] Cronologia Analisi"):
        try:
            history = get_analysis_history(limit=10)
            if history:
                st.sidebar.markdown("### Ultime Analisi:")
                for i, analysis in enumerate(history[:5], 1):
                    st.sidebar.markdown(f"**{i}.** {analysis['title'][:25]}...")
                    st.sidebar.markdown(f"Score: {analysis['score']}")
            else:
                st.sidebar.info("Nessuna analisi trovata")
        except Exception as e:
            st.sidebar.error(f"Errore: {e}")

def render_metrics_overview():
    """Rende la sezione metriche generali"""
    st.header("[REPORT] Panoramica Metriche")
    
    # Metriche di esempio (in produzione verrebbero dal database)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Video Analizzati",
            value="156",
            delta="+12 questa settimana"
        )
    
    with col2:
        st.metric(
            label="Score Medio",
            value="78.5",
            delta="+2.3"
        )
    
    with col3:
        st.metric(
            label="Agenti Utilizzati",
            value="3",
            delta=""
        )
    
    with col4:
        st.metric(
            label="Report Generati",
            value="23",
            delta="+5 questo mese"
        )

def render_analytics_charts():
    """Rende i grafici analytics"""
    st.header("[REPORT] Analytics Avanzati")
    
    # Dati di esempio
    dates = pd.date_range(start='2024-01-01', end='2024-12-24', freq='D')
    scores = [70 + i * 0.5 + (i % 7) * 2 for i in range(len(dates))]
    
    df = pd.DataFrame({
        'Data': dates,
        'Score': scores,
        'Engagement': [3.5 + (i % 5) * 0.3 for i in range(len(dates))],
        'Completion': [65 + (i % 10) * 2 for i in range(len(dates))]
    })
    
    # Grafico trend score
    col1, col2 = st.columns(2)
    
    with col1:
        fig_score = px.line(
            df, x='Data', y='Score',
            title="Trend Score nel Tempo",
            labels={'Score': 'Punteggio', 'Data': 'Data'}
        )
        fig_score.update_layout(height=400)
        st.plotly_chart(fig_score, use_container_width=True)
    
    with col2:
        fig_engagement = px.scatter(
            df, x='Engagement', y='Completion',
            title="Engagement vs Completion Rate",
            labels={'Engagement': 'Tasso Engagement', 'Completion': 'Completion Rate'}
        )
        fig_engagement.update_layout(height=400)
        st.plotly_chart(fig_engagement, use_container_width=True)

def render_chat_interface():
    """Rende l'interfaccia chat integrata"""
    st.header("[CHAT] Chat con Agenti AI")
    
    if not PRO_FEATURES_AVAILABLE:
        st.warning("Chat non disponibile senza funzionalità Pro")
        return
    
    # Inizializza chat
    chat = AgentChat()
    
    # Area chat
    chat_container = st.container()
    
    with chat_container:
        # Mostra messaggi esistenti
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])
        
        # Input utente
        if prompt := st.chat_input("Scrivi il tuo messaggio..."):
            # Aggiungi messaggio utente
            st.session_state.chat_messages.append({
                "role": "user",
                "content": prompt,
                "avatar": "[USER]",
                "timestamp": datetime.now()
            })
            
            # Mostra messaggio utente
            with st.chat_message("user", avatar="[USER]"):
                st.markdown(prompt)
            
            # Genera risposta agente
            agent_response = chat.get_agent_response(
                st.session_state.selected_agent, 
                prompt
            )
            
            # Aggiungi risposta agente
            selected_agent_info = chat.agents[st.session_state.selected_agent]
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": agent_response,
                "avatar": selected_agent_info["avatar"],
                "timestamp": datetime.now()
            })
            
            # Mostra risposta agente
            with st.chat_message("assistant", avatar=selected_agent_info["avatar"]):
                st.markdown(agent_response)
    
    # Controlli chat
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Cancella Chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col2:
        if st.button("💾 Salva Chat"):
            if st.session_state.chat_messages:
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "agent": st.session_state.selected_agent,
                    "messages": st.session_state.chat_messages
                }
                st.download_button(
                    label="[INFO] Scarica JSON",
                    data=json.dumps(chat_data, indent=2, default=str),
                    file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    with col3:
        if st.button("[INFO] Nuova Sessione"):
            st.session_state.chat_messages = []
            st.rerun()

def render_quick_actions():
    """Rende le azioni rapide"""
    st.header("[ACTIONS] Azioni Rapide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("[ANALYTICS] Analytics")
        if st.button("[REPORT] Genera Report Completo"):
            try:
                # Crea report completo
                report_data = {
                    "video_title": "Report Completo TokIntel Pro",
                    "analysis_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "overall_score": 85,
                    "summary": "Report completo generato dalla dashboard Pro",
                    "key_points": [
                        "Dashboard integrata con AI Agents",
                        "Analytics avanzati e metriche",
                        "Esportazione PDF professionale",
                        "Database PostgreSQL completo"
                    ],
                    "metrics": {
                        "engagement_rate": 4.5,
                        "completion_rate": 78,
                        "share_rate": 2.3,
                        "comment_rate": 1.9,
                        "like_rate": 3.8
                    },
                    "keywords": ["tokintel", "pro", "dashboard", "ai", "analytics"],
                    "suggested_hashtags": ["#tokintelpro", "#ai", "#analytics", "#dashboard"],
                    "recommendations": [
                        {
                            "title": "Usa la Dashboard Pro",
                            "description": "Sfrutta tutte le funzionalità avanzate per ottimizzare i tuoi contenuti."
                        },
                        {
                            "title": "Interagisci con gli Agenti",
                            "description": "Parla con gli esperti AI per consigli personalizzati."
                        }
                    ]
                }
                
                pdf_path = export_analysis_to_pdf(report_data)
                st.success(f"[OK] Report completo generato: {pdf_path}")
                
            except Exception as e:
                st.error(f"[ERROR] Errore: {e}")
    
    with col2:
        st.subheader("[AGENTS] AI Agents")
        if st.button("[STRATEGIST] Consiglio Strategist"):
            if PRO_FEATURES_AVAILABLE:
                chat = AgentChat()
                response = chat.get_agent_response("strategist", "Dammi un consiglio strategico per TikTok")
                st.info(f"[STRATEGIST] {response}")
            else:
                st.warning("Agenti AI non disponibili")
        
        if st.button("[COPYWRITER] Consiglio Copywriter"):
            if PRO_FEATURES_AVAILABLE:
                chat = AgentChat()
                response = chat.get_agent_response("copywriter", "Come scrivere un hook efficace?")
                st.info(f"[COPYWRITER] {response}")
            else:
                st.warning("Agenti AI non disponibili")
    
    with col3:
        st.subheader("[DB] Database")
        if st.button("[HISTORY] Mostra Cronologia"):
            try:
                history = get_analysis_history(limit=5)
                if history:
                    st.markdown("### Ultime 5 Analisi:")
                    for i, analysis in enumerate(history, 1):
                        st.markdown(f"**{i}.** {analysis['title']}")
                        st.markdown(f"Score: {analysis['score']} | {analysis['created_at'][:10]}")
                else:
                    st.info("Nessuna analisi nel database")
            except Exception as e:
                st.error(f"Errore database: {e}")

def render_system_status():
    """Rende lo stato del sistema"""
    st.header("[STATUS] Stato Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("[MODULES] Moduli")
        
        # Verifica moduli
        modules_status = {
            "Chat Agents": PRO_FEATURES_AVAILABLE,
            "PDF Exporter": PRO_FEATURES_AVAILABLE,
            "Database": PRO_FEATURES_AVAILABLE,
            "Analytics": True
        }
        
        for module, status in modules_status.items():
            if status:
                st.success(f"[OK] {module}")
            else:
                st.error(f"[ERROR] {module}")
    
    with col2:
        st.subheader("[STATS] Statistiche")
        
        # Statistiche di sistema
        stats = {
            "Sessione attiva": "Sì",
            "Memoria utilizzata": "~45MB",
            "Tempo di avvio": "2.3s",
            "Versione Python": "3.8+"
        }
        
        for stat, value in stats.items():
            st.metric(stat, value)

def main():
    """Funzione principale della dashboard Pro"""
    
    # Inizializza stato sessione
    init_session_state()
    
    # Rendi header
    render_header()
    
    # Rendi sidebar
    render_sidebar()
    
    # Controlla se le funzionalità Pro sono disponibili
    if not PRO_FEATURES_AVAILABLE:
        st.warning("""
        [WARN]️ **Funzionalità Pro non disponibili**
        
        Per utilizzare tutte le funzionalità:
        1. Installa le dipendenze: `pip install -r requirements_pro.txt`
        2. Riavvia l'applicazione
        """)
    
    # Tabs principali
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "[REPORT] Dashboard", "💬 Chat AI", "[REPORT] Analytics", "⚡ Azioni", "[INFO] Sistema"
    ])
    
    with tab1:
        render_metrics_overview()
        render_analytics_charts()
    
    with tab2:
        render_chat_interface()
    
    with tab3:
        st.header("[REPORT] Analytics Dettagliati")
        st.info("Sezione analytics avanzati - In sviluppo")
        
        # Placeholder per analytics futuri
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Performance Trends")
            # Grafico placeholder
            chart_data = pd.DataFrame({
                'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag'],
                'Score': [75, 78, 82, 79, 85]
            })
            fig = px.line(chart_data, x='Mese', y='Score', title="Trend Score Mensile")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏷️ Top Keywords")
            keywords_data = pd.DataFrame({
                'Keyword': ['tiktok', 'viral', 'content', 'trending', 'engagement'],
                'Frequenza': [45, 32, 28, 25, 22]
            })
            fig = px.bar(keywords_data, x='Frequenza', y='Keyword', orientation='h', title="Keywords Più Usate")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        render_quick_actions()
    
    with tab5:
        render_system_status()
    
    # Footer
    st.markdown("---")
    st.markdown("*TokIntel v2.1 Pro+ Dashboard - Potenzia la tua strategia TikTok con AI avanzata*")

if __name__ == "__main__":
    main() 