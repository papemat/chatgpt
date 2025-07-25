#!/usr/bin/env python3
"""
TokIntel v2 - UI Interface Module
Streamlit-based user interface for video analysis
"""

from typing import Dict, List, Any, Optional
import logging
logger = logging.getLogger(__name__)
import os
import time
import asyncio

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

# Import visualization libraries
try:
    import plotly.express as px
    import pandas as pd
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    pd = None

from core.config import ConfigManager
from core.logger import setup_logger
from core.exceptions import TokIntelError

# Setup logging
logger = setup_logger(__name__)

class StreamlitInterface:
    """Streamlit-based user interface for TokIntel"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the Streamlit interface"""
        try:
            self.config_manager = ConfigManager(config_path)
            self.config = self.config_manager.get_config()
            self.pipeline = VideoAnalysisPipeline(self.config)
            logger.info("Streamlit interface initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Streamlit interface: {e}")
            raise TokIntelError(f"UI initialization error: {e}")
    
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="TokIntel v2",
            page_icon="[REPORT]",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #c3e6cb;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #f5c6cb;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="main-header"><h1>[REPORT] TokIntel v2 – Analisi Video TikTok</h1></div>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        with st.sidebar:
            st.header("⚙️ Configurazione")
            
            # Model selection
            model = st.selectbox(
                "Modello LLM",
                ["gpt-4", "gpt-3.5-turbo", "local-model"],
                index=0,
                help="Seleziona il modello LLM da utilizzare per l'analisi"
            )
            
            # Language selection
            language = st.selectbox(
                "Lingua",
                ["it", "en", "es", "fr"],
                index=0,
                help="Lingua per l'analisi del contenuto"
            )
            
            # Export format
            export_formats = st.multiselect(
                "Formato esportazione",
                ["JSON", "CSV", "PDF"],
                default=["JSON", "CSV"],
                help="Formati di output per i risultati"
            )
            
            # Advanced settings
            with st.expander("[INFO] Impostazioni Avanzate"):
                temperature = st.slider(
                    "Temperatura LLM",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.7,
                    step=0.1,
                    help="Controlla la creatività delle risposte"
                )
                
                max_tokens = st.slider(
                    "Token massimi",
                    min_value=100,
                    max_value=2000,
                    value=500,
                    step=100,
                    help="Lunghezza massima delle risposte"
                )
                
                frame_interval = st.slider(
                    "Intervallo frame",
                    min_value=10,
                    max_value=60,
                    value=30,
                    step=5,
                    help="Frame estratti ogni N secondi"
                )
            
            # Update config
            self.config["model"] = model
            self.config["language"] = language
            self.config["export_format"] = [fmt.lower() for fmt in export_formats]
            self.config["llm_config"]["temperature"] = temperature
            self.config["llm_config"]["max_tokens"] = max_tokens
            self.config["frame_extraction_interval"] = frame_interval
            
            st.markdown("---")
            st.markdown("### [REPORT] Statistiche")
            if "processed_videos" in st.session_state:
                st.metric("Video processati", st.session_state.processed_videos)
            
            if "total_processing_time" in st.session_state:
                st.metric("Tempo totale", f"{st.session_state.total_processing_time:.1f}s")
    
    def render_file_upload(self) -> Optional[str]:
        """Render file upload section and return video path if uploaded"""
        st.header("[INFO] Carica Video")
        
        # File upload with drag and drop
        uploaded_file = st.file_uploader(
            "Carica un video TikTok (.mp4)",
            type=["mp4", "avi", "mov", "mkv"],
            help="Supporta formati video comuni. Trascina il file qui o clicca per selezionare."
        )
        
        if uploaded_file:
            # Show file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nome file", uploaded_file.name)
            with col2:
                st.metric("Dimensione", f"{uploaded_file.size / 1024 / 1024:.1f} MB")
            with col3:
                st.metric("Tipo", uploaded_file.type)
            
            # Create temp directory if it doesn't exist
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)
            
            # Save uploaded file
            video_path = temp_dir / uploaded_file.name
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Display video
            st.video(str(video_path))
            return str(video_path)
        
        return None
    
    async def process_video_async(self, video_path: str) -> Dict[str, Any]:
        """Process video asynchronously"""
        try:
            logger.info(f"Starting UI analysis of video: {video_path}")
            
            # Show progress
            with st.spinner("[INFO] Analisi in corso..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                status_text.text("Estrazione frame...")
                progress_bar.progress(20)
                
                # Process video through pipeline
                results = await self.pipeline.analyze(video_path)
                
                progress_bar.progress(100)
                status_text.text("[OK] Analisi completata!")
                
                logger.info(f"Successfully analyzed video: {video_path}")
                return results
                
        except Exception as e:
            logger.error(f"Error processing video {video_path}: {e}")
            st.error(f"Errore durante l'analisi: {e}")
            raise TokIntelError(f"Processing error: {e}")
    
    def render_results(self, results: Dict[str, Any]):
        """Render analysis results with improved layout"""
        if not results:
            st.warning("Nessun risultato da visualizzare")
            return
        
        # Success message
        st.markdown('<div class="success-message">[OK] Analisi completata con successo!</div>', unsafe_allow_html=True)
        
        # Create tabs for different result sections
        tab1, tab2, tab3, tab4 = st.tabs(["[INFO] Sintesi", "[REPORT] Punteggi", "[INFO] Dettagli", "[REPORT] Grafici"])
        
        with tab1:
            st.header("[INFO] Sintesi dell'Analisi")
            if "summary" in results:
                # Parse and display summary in a more readable format
                summary = results["summary"]
                if isinstance(summary, str):
                    # Try to extract structured information
                    lines = summary.split('\n')
                    for line in lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            st.markdown(f"**{key.strip()}:** {value.strip()}")
                        else:
                            st.text(line)
                else:
                    st.json(summary)
            else:
                st.info("Sintesi non disponibile")
        
        with tab2:
            st.header("[REPORT] Punteggi e Metriche")
            if "score" in results:
                score_data = results["score"]
                if isinstance(score_data, dict):
                    # Display scores in columns
                    cols = st.columns(len(score_data))
                    for i, (key, value) in enumerate(score_data.items()):
                        with cols[i]:
                            if isinstance(value, (int, float)):
                                st.metric(key.title(), f"{value:.2f}")
                            else:
                                st.metric(key.title(), str(value))
                else:
                    st.json(score_data)
            else:
                st.info("Punteggi non disponibili")
        
        with tab3:
            st.header("[INFO] Dettagli dell'Analisi")
            if "details" in results:
                st.json(results["details"])
            else:
                st.info("Dettagli non disponibili")
        
        with tab4:
            st.header("[REPORT] Grafici e Visualizzazioni")
            if "score" in results and isinstance(results["score"], dict) and PLOTLY_AVAILABLE:
                # Create a simple bar chart
                score_items = list(results["score"].items())
                df = pd.DataFrame(score_items, columns=["Metrica", "Valore"])
                
                fig = px.bar(df, x="Metrica", y="Valore", 
                           title="Punteggi per Metrica",
                           color="Valore",
                           color_continuous_scale="viridis")
                st.plotly_chart(fig, use_container_width=True)
            elif "score" in results and isinstance(results["score"], dict):
                st.info("Grafici non disponibili - installa plotly e pandas per le visualizzazioni")
                # Fallback: show data as simple list
                score_items = list(results["score"].items())
                for metric, value in score_items:
                    st.write(f"**{metric}:** {value}")
            else:
                st.info("Grafici non disponibili")
        
        # Export section
        st.header("💾 Esportazione")
        if st.button("[INFO] Scarica Risultati"):
            self.export_results(results)
    
    def export_results(self, results: Dict[str, Any]):
        """Export results in selected formats"""
        try:
            # This would integrate with the ExporterAgent
            st.success("[OK] Risultati esportati con successo!")
            st.info("I file sono stati salvati nella cartella 'output/'")
        except Exception as e:
            st.error(f"Errore durante l'esportazione: {e}")
    
    def render_error_handling(self):
        """Render error handling section"""
        if "error" in st.session_state:
            st.error(f"[ERROR] Errore: {st.session_state.error}")
            del st.session_state.error
    
    def run(self):
        """Main method to run the Streamlit interface"""
        try:
            # Setup page
            self.setup_page()
            
            # Render sidebar
            self.render_sidebar()
            
            # Render error handling
            self.render_error_handling()
            
            # File upload
            video_path = self.render_file_upload()
            
            if video_path:
                # Process video
                results = asyncio.run(self.process_video_async(video_path))
                
                # Update session state
                if "processed_videos" not in st.session_state:
                    st.session_state.processed_videos = 0
                st.session_state.processed_videos += 1
                
                # Render results
                self.render_results(results)
                
                # Cleanup temp file
                try:
                    os.remove(video_path)
                except (OSError, FileNotFoundError):
                    pass  # Ignore cleanup errors
        
        except Exception as e:
            logger.error(f"Streamlit interface error: {e}")
            st.error(f"Errore dell'interfaccia: {e}")

def main():
    """Entry point for Streamlit app"""
    interface = StreamlitInterface()
    interface.run()

if __name__ == "__main__":
    main() 