#!/usr/bin/env python3
"""
TokIntel v2 - TikTok Library Dashboard
Dashboard per visualizzare, filtrare e rianalizzare i video salvati
"""

import streamlit as st
import asyncio
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import io

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from scraper.download_tiktok_video import TikTokVideoDownloader, get_user_cached_videos
from db.database import DatabaseManager, get_db_manager
from core.config import ConfigManager
from core.logger import setup_logger

logger = setup_logger(__name__)

class TikTokLibraryDashboard:
    """Dashboard per la gestione della libreria TikTok"""
    
    def __init__(self):
        """Inizializza la dashboard"""
        self.db_manager = get_db_manager()
        self.config_manager = ConfigManager()
        self.downloader = TikTokVideoDownloader()
        
    def setup_page(self):
        """Configura la pagina Streamlit"""
        st.set_page_config(
            page_title="My TikTok Library - TokIntel v2",
            page_icon="[INFO]",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .library-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .video-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .metric-badge {
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-analyzed { background: #d4edda; color: #155724; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-error { background: #f8d7da; color: #721c24; }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="library-header"><h1>[INFO] My TikTok Library</h1><p>Gestisci e analizza i tuoi video salvati</p></div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Rende la sidebar con filtri e opzioni"""
        with st.sidebar:
            st.header("[INFO] Filtri e Opzioni")
            
            # Filtri temporali
            st.subheader("📅 Periodo")
            date_filter = st.selectbox(
                "Filtra per data",
                ["Tutti", "Ultimi 7 giorni", "Ultimi 30 giorni", "Ultimi 3 mesi", "Ultimo anno"]
            )
            
            # Filtri per stato
            st.subheader("[REPORT] Stato Analisi")
            status_filter = st.multiselect(
                "Filtra per stato",
                ["new", "analyzed", "error"],
                default=["new", "analyzed", "error"],
                format_func=lambda x: {
                    "new": "[WARN] Nuovo",
                    "analyzed": "[OK] Analizzato", 
                    "error": "[ERROR] Errore"
                }.get(x, x)
            )
            
            # Filtri per punteggio
            st.subheader("⭐ Punteggio")
            min_score = st.slider("Punteggio minimo", 0.0, 10.0, 0.0, 0.5)
            max_score = st.slider("Punteggio massimo", 0.0, 10.0, 10.0, 0.5)
            
            # Opzioni di ordinamento
            st.subheader("[INFO] Ordinamento")
            sort_by = st.selectbox(
                "Ordina per",
                ["Data download", "Punteggio", "Dimensione file", "Nome file"]
            )
            sort_order = st.selectbox("Ordine", ["Decrescente", "Crescente"])
            
            # Azioni batch
            st.subheader("⚡ Azioni Rapide")
            if st.button("[INFO] Aggiorna Cache", type="primary"):
                st.session_state.refresh_cache = True
            
            if st.button("🗑️ Pulisci Cache"):
                st.session_state.clear_cache = True
            
            # Auto-analisi batch
            st.divider()
            st.subheader("[REPORT] Auto-Analisi")
            
            # Mostra statistiche status
            try:
                from batch_auto_analyze import get_user_analysis_summary
                summary = get_user_analysis_summary(user_id=1)  # Per ora fisso a 1
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("[WARN] Nuovi", summary.get('new_videos', 0))
                with col2:
                    st.metric("[OK] Analizzati", summary.get('analyzed_videos', 0))
                
                if summary.get('new_videos', 0) > 0:
                    if st.button("[INFO] Analizza Tutti i Nuovi Video", type="primary"):
                        st.session_state.start_batch_analysis = True
                else:
                    st.info("Nessun video nuovo da analizzare")
                    
            except Exception as e:
                st.error(f"Errore nel caricamento statistiche: {e}")
            
            # Statistiche cache
            st.subheader("[REPORT] Statistiche Cache")
            cache_stats = self.downloader.get_cache_stats()
            st.metric("Video totali", cache_stats.get('total_videos', 0))
            st.metric("Dimensione totale", f"{cache_stats.get('total_size_mb', 0)} MB")
            
            return {
                'date_filter': date_filter,
                'status_filter': status_filter,
                'min_score': min_score,
                'max_score': max_score,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
    
    async def get_video_data(self, user_id: int = 1) -> List[Dict[str, Any]]:
        """Ottiene i dati dei video dal database con status"""
        try:
            # Ottieni video dal database con status
            videos_with_analysis = self.db_manager.get_videos_with_analysis(user_id)
            
            # Converti in formato compatibile
            video_data = []
            for video in videos_with_analysis:
                # Determina status display
                status_display = {
                    'new': '[WARN] Nuovo',
                    'analyzed': '[OK] Analizzato',
                    'error': '[ERROR] Errore'
                }.get(video['status'], video['status'])
                
                # Determina score
                score = None
                analysis_id = None
                if video['analysis']:
                    score = video['analysis'].get('overall_score')
                    analysis_id = video['analysis'].get('id')
                
                video_data.append({
                    'video_id': video['tiktok_video_id'],
                    'file_path': video['local_file_path'],
                    'file_size_mb': video['file_size_mb'],
                    'metadata': {
                        'title': video['video_title'],
                        'creator': video['creator_username'],
                        'download_timestamp': video['saved_at'].isoformat() if video['saved_at'] else None,
                        'original_url': video['video_url']
                    },
                    'status': video['status'],  # new, analyzed, error
                    'status_display': status_display,
                    'score': score,
                    'analysis_id': analysis_id,
                    'download_date': video['saved_at'],
                    'original_url': video['video_url'],
                    'video_title': video['video_title'],
                    'creator_username': video['creator_username']
                })
            
            return video_data
            
        except Exception as e:
            logger.error(f"Error getting video data: {e}")
            return []
    
    def apply_filters(self, videos: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Applica i filtri ai video"""
        filtered_videos = videos.copy()
        
        # Filtro per stato
        if filters['status_filter']:
            filtered_videos = [v for v in filtered_videos if v['status'] in filters['status_filter']]
        
        # Filtro per punteggio
        filtered_videos = [v for v in filtered_videos 
                          if v['score'] is None or 
                          (filters['min_score'] <= v['score'] <= filters['max_score'])]
        
        # Filtro per data
        if filters['date_filter'] != "Tutti":
            now = datetime.utcnow()
            if filters['date_filter'] == "Ultimi 7 giorni":
                cutoff = now - timedelta(days=7)
            elif filters['date_filter'] == "Ultimi 30 giorni":
                cutoff = now - timedelta(days=30)
            elif filters['date_filter'] == "Ultimi 3 mesi":
                cutoff = now - timedelta(days=90)
            elif filters['date_filter'] == "Ultimo anno":
                cutoff = now - timedelta(days=365)
            
            filtered_videos = [v for v in filtered_videos 
                              if v['download_date'] and 
                              datetime.fromisoformat(v['download_date'].replace('Z', '+00:00')) > cutoff]
        
        # Ordinamento
        reverse = filters['sort_order'] == "Decrescente"
        if filters['sort_by'] == "Data download":
            filtered_videos.sort(key=lambda x: x['download_date'] or "", reverse=reverse)
        elif filters['sort_by'] == "Punteggio":
            filtered_videos.sort(key=lambda x: x['score'] or 0, reverse=reverse)
        elif filters['sort_by'] == "Dimensione file":
            filtered_videos.sort(key=lambda x: x['file_size_mb'] or 0, reverse=reverse)
        elif filters['sort_by'] == "Nome file":
            filtered_videos.sort(key=lambda x: x['video_id'], reverse=reverse)
        
        return filtered_videos
    
    def render_video_grid(self, videos: List[Dict[str, Any]]):
        """Rende la griglia dei video"""
        if not videos:
            st.info("Nessun video trovato con i filtri applicati.")
            return
        
        # Layout a colonne
        cols = st.columns(3)
        
        for i, video in enumerate(videos):
            col_idx = i % 3
            with cols[col_idx]:
                self.render_video_card(video)
    
    def render_video_card(self, video: Dict[str, Any]):
        """Rende una card per un singolo video"""
        with st.container():
            st.markdown(f"""
            <div class="video-card">
                <h4>[VIDEO] {video.get('video_title', video['video_id'][:20])}</h4>
                <p><strong>Stato:</strong> <span class="status-badge status-{video['status']}">{video['status_display']}</span></p>
                <p><strong>Creatore:</strong> {video.get('creator_username', 'N/A')}</p>
                <p><strong>Dimensione:</strong> {video['file_size_mb']} MB</p>
                <p><strong>Data:</strong> {video['download_date'].strftime('%Y-%m-%d') if video['download_date'] else 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Punteggio se disponibile
            if video['score'] is not None:
                st.metric("Punteggio", f"{video['score']:.1f}/10")
            
            # Azioni per video
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("[PREVIEW] Anteprima", key=f"preview_{video['video_id']}"):
                    self.show_video_preview(video)
            
            with col2:
                if st.button("[REANALYZE] Rianalizza", key=f"reanalyze_{video['video_id']}"):
                    st.session_state.reanalyze_video = video
            
            with col3:
                if st.button("[REMOVE] Rimuovi", key=f"remove_{video['video_id']}"):
                    st.session_state.remove_video = video
    
    def show_video_preview(self, video: Dict[str, Any]):
        """Mostra l'anteprima del video"""
        try:
            video_path = Path(video['file_path'])
            if video_path.exists():
                with open(video_path, "rb") as f:
                    video_bytes = f.read()
                
                st.video(video_bytes)
            else:
                st.error("File video non trovato")
        except Exception as e:
            st.error(f"Errore nel caricamento del video: {e}")
    
    def render_analytics(self, videos: List[Dict[str, Any]]):
        """Rende le analytics della libreria"""
        st.header("[REPORT] Analytics Libreria")
        
        if not videos:
            st.info("Nessun dato disponibile per le analytics.")
            return
        
        # Statistiche generali
        col1, col2, col3, col4 = st.columns(4)
        
        total_videos = len(videos)
        analyzed_videos = len([v for v in videos if v['status'] == 'analyzed'])
        total_size = sum(v['file_size_mb'] for v in videos)
        avg_score = sum(v['score'] or 0 for v in videos if v['score'] is not None) / max(1, analyzed_videos)
        
        with col1:
            st.metric("Video Totali", total_videos)
        with col2:
            st.metric("Analizzati", analyzed_videos)
        with col3:
            st.metric("Dimensione Totale", f"{total_size:.1f} MB")
        with col4:
            st.metric("Punteggio Medio", f"{avg_score:.1f}/10")
        
        # Grafici
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuzione punteggi
            scores = [v['score'] for v in videos if v['score'] is not None]
            if scores:
                fig = px.histogram(
                    x=scores,
                    nbins=10,
                    title="Distribuzione Punteggi",
                    labels={'x': 'Punteggio', 'y': 'Numero Video'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Video per stato
            status_counts = {}
            for video in videos:
                status = video['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                fig = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="Video per Stato"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Timeline download
        st.subheader("📅 Timeline Download")
        download_dates = [v['download_date'][:10] for v in videos if v['download_date']]
        if download_dates:
            date_counts = pd.Series(download_dates).value_counts().sort_index()
            fig = px.line(
                x=date_counts.index,
                y=date_counts.values,
                title="Video scaricati nel tempo",
                labels={'x': 'Data', 'y': 'Numero Video'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_export_options(self, videos: List[Dict[str, Any]]):
        """Rende le opzioni di esportazione"""
        st.header("[INFO] Esportazione")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Esporta Dati")
            
            if st.button("[INFO] Esporta JSON"):
                self.export_to_json(videos)
            
            if st.button("[REPORT] Esporta CSV"):
                self.export_to_csv(videos)
            
            if st.button("[INFO] Esporta PDF"):
                self.export_to_pdf(videos)
        
        with col2:
            st.subheader("Esporta Video")
            
            selected_videos = st.multiselect(
                "Seleziona video da esportare",
                [v['video_id'] for v in videos],
                format_func=lambda x: x[:20] + "..."
            )
            
            if st.button("[INFO] Scarica Selezionati"):
                self.download_selected_videos(selected_videos, videos)
    
    def export_to_json(self, videos: List[Dict[str, Any]]):
        """Esporta i dati in formato JSON"""
        try:
            export_data = []
            for video in videos:
                export_data.append({
                    'video_id': video['video_id'],
                    'status': video['status'],
                    'score': video['score'],
                    'file_size_mb': video['file_size_mb'],
                    'download_date': video['download_date'],
                    'original_url': video['original_url']
                })
            
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="[INFO] Scarica JSON",
                data=json_str,
                file_name=f"tiktok_library_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Errore nell'esportazione JSON: {e}")
    
    def export_to_csv(self, videos: List[Dict[str, Any]]):
        """Esporta i dati in formato CSV"""
        try:
            df = pd.DataFrame(videos)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="[INFO] Scarica CSV",
                data=csv,
                file_name=f"tiktok_library_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Errore nell'esportazione CSV: {e}")
    
    def export_to_pdf(self, videos: List[Dict[str, Any]]):
        """Esporta i dati in formato PDF"""
        try:
            # Implementazione base - in produzione usare reportlab o weasyprint
            st.info("Funzionalità PDF in sviluppo. Usa JSON o CSV per ora.")
        except Exception as e:
            st.error(f"Errore nell'esportazione PDF: {e}")
    
    def download_selected_videos(self, selected_ids: List[str], videos: List[Dict[str, Any]]):
        """Scarica i video selezionati"""
        try:
            # Implementazione per download multiplo
            st.info(f"Download di {len(selected_ids)} video in preparazione...")
            # In produzione, creare un ZIP con i video selezionati
        except Exception as e:
            st.error(f"Errore nel download: {e}")
    
    def render_analysis_history(self, user_id: int = 1):
        """Rende la cronologia delle analisi"""
        st.header("[INFO] Cronologia Analisi")
        
        try:
            with self.db_manager.get_session() as session:
                analyses = self.db_manager.get_user_analyses(user_id, limit=50)
            
            if not analyses:
                st.info("Nessuna analisi trovata.")
                return
            
            # Tabella cronologia
            history_data = []
            for analysis in analyses:
                history_data.append({
                    'ID': analysis.id,
                    'Titolo': analysis.video_title,
                    'Punteggio': f"{analysis.overall_score:.1f}/10",
                    'Data': analysis.created_at.strftime('%Y-%m-%d %H:%M'),
                    'Stato': 'Completata'
                })
            
            df = pd.DataFrame(history_data)
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Errore nel caricamento della cronologia: {e}")
    
    def run(self):
        """Esegue la dashboard"""
        self.setup_page()
        
        # Gestione session state
        if 'refresh_cache' not in st.session_state:
            st.session_state.refresh_cache = False
        if 'clear_cache' not in st.session_state:
            st.session_state.clear_cache = False
        if 'reanalyze_video' not in st.session_state:
            st.session_state.reanalyze_video = None
        if 'remove_video' not in st.session_state:
            st.session_state.remove_video = None
        if 'start_batch_analysis' not in st.session_state:
            st.session_state.start_batch_analysis = False
        if 'batch_analysis_progress' not in st.session_state:
            st.session_state.batch_analysis_progress = 0
        if 'batch_analysis_message' not in st.session_state:
            st.session_state.batch_analysis_message = ""
        
        # Sidebar
        filters = self.render_sidebar()
        
        # Gestione azioni
        if st.session_state.refresh_cache:
            st.success("Cache aggiornata!")
            st.session_state.refresh_cache = False
        
        if st.session_state.clear_cache:
            if st.button("Conferma pulizia cache"):
                self.downloader.clear_cache()
                st.success("Cache pulita!")
                st.session_state.clear_cache = False
        
        if st.session_state.reanalyze_video:
            video = st.session_state.reanalyze_video
            st.info(f"Rianalisi video {video['video_id']} in corso...")
            # Implementare rianalisi
            st.session_state.reanalyze_video = None
        
        if st.session_state.remove_video:
            video = st.session_state.remove_video
            if st.button(f"Conferma rimozione video {video['video_id']}"):
                self.downloader.clear_cache(video['video_id'])
                st.success("Video rimosso!")
                st.session_state.remove_video = None
        
        # Gestione auto-analisi batch
        if st.session_state.start_batch_analysis:
            st.session_state.start_batch_analysis = False
            
            # Mostra progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                from batch_auto_analyze import analyze_user_pending_videos
                
                def progress_callback(progress, message):
                    progress_bar.progress(progress / 100)
                    status_text.text(message)
                
                # Esegui analisi batch
                results = asyncio.run(analyze_user_pending_videos(1, progress_callback))
                
                # Mostra risultati
                progress_bar.progress(100)
                status_text.text("Analisi completata!")
                
                if results['success']:
                    st.success(f"[OK] Analisi batch completata: {results['analyzed']} video analizzati, {results['errors']} errori")
                    st.json(results)
                else:
                    st.error(f"[ERRORE] Errore nell'analisi batch: {results.get('error', 'Errore sconosciuto')}")
                    
            except Exception as e:
                st.error(f"Errore nell'analisi batch: {e}")
                logger.error(f"Errore auto-analisi batch: {e}")
        
        # Contenuto principale
        tabs = st.tabs(["[INFO] Libreria", "[REPORT] Analytics", "[INFO] Esportazione", "[INFO] Cronologia"])
        
        with tabs[0]:
            st.header("[INFO] La tua Libreria TikTok")
            
            # Carica dati video
            videos = asyncio.run(self.get_video_data())
            
            # Applica filtri
            filtered_videos = self.apply_filters(videos, filters)
            
            # Mostra risultati
            st.write(f"**{len(filtered_videos)}** video trovati")
            
            # Vista griglia
            self.render_video_grid(filtered_videos)
        
        with tabs[1]:
            self.render_analytics(videos)
        
        with tabs[2]:
            self.render_export_options(videos)
        
        with tabs[3]:
            self.render_analysis_history()

def main():
    """Funzione principale"""
    try:
        dashboard = TikTokLibraryDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Errore nell'avvio della dashboard: {e}")
        logger.error(f"Dashboard error: {e}")

if __name__ == "__main__":
    main() 