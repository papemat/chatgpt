#!/usr/bin/env python3
"""
TokIntel v2 - TikTok Import Interface
Interfaccia Streamlit per login TikTok e importazione video salvati
"""

import streamlit as st
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from auth.tiktok_oauth import TikTokOAuth
from scraper.tiktok_saves import TikTokSavesScraper
from core.logger import setup_logger

logger = setup_logger(__name__)

class TikTokImportInterface:
    """Interfaccia Streamlit per importazione TikTok"""
    
    def __init__(self):
        """Inizializza l'interfaccia"""
        self.oauth_client = None
        self.scraper = None
        self.setup_page()
    
    def setup_page(self):
        """Configura pagina Streamlit"""
        st.set_page_config(
            page_title="TokIntel - TikTok Import",
            page_icon="🎵",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .tiktok-header {
            background: linear-gradient(90deg, #ff0050 0%, #00f2ea 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .login-card {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            margin-bottom: 1rem;
        }
        .video-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .success-badge {
            background: #d4edda;
            color: #155724;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
        }
        .error-badge {
            background: #f8d7da;
            color: #721c24;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="tiktok-header"><h1>🎵 TokIntel - Import TikTok</h1><p>Importa i tuoi video salvati e collezioni per l\'analisi</p></div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Renderizza sidebar con opzioni"""
        with st.sidebar:
            st.header("⚙️ Opzioni Import")
            
            # Modalità import
            import_mode = st.selectbox(
                "Modalità Import",
                ["Login TikTok", "Link Manuali"],
                help="Scegli come importare i video"
            )
            
            # Numero massimo video
            max_videos = st.slider(
                "Numero massimo video",
                min_value=10,
                max_value=200,
                value=50,
                help="Limita il numero di video da importare"
            )
            
            # Opzioni avanzate
            with st.expander("Opzioni Avanzate"):
                use_fallback = st.checkbox(
                    "Usa API Fallback",
                    value=False,
                    help="Usa endpoint alternativi se l'API principale non funziona"
                )
                
                headless_mode = st.checkbox(
                    "Modalità Headless",
                    value=True,
                    help="Esegui browser in background"
                )
                
                slow_mo = st.slider(
                    "Velocità Scraping (ms)",
                    min_value=50,
                    max_value=500,
                    value=100,
                    help="Ritardo tra azioni di scraping"
                )
            
            st.markdown("---")
            st.markdown("### [REPORT] Statistiche")
            
            # Statistiche sessione
            if 'imported_videos' in st.session_state:
                st.metric("Video Importati", len(st.session_state.imported_videos))
            
            if 'imported_collections' in st.session_state:
                st.metric("Collezioni", len(st.session_state.imported_collections))
    
    def render_login_section(self):
        """Renderizza sezione login TikTok"""
        st.header("[INFO] Login TikTok")
        
        # Inizializza OAuth client
        if not self.oauth_client:
            try:
                self.oauth_client = TikTokOAuth()
            except Exception as e:
                st.error(f"Errore inizializzazione OAuth: {e}")
                return
        
        # Verifica stato autenticazione
        auth_status = self.oauth_client.get_auth_status()
        
        if auth_status['authenticated']:
            st.success("[OK] Autenticato con TikTok")
            
            if auth_status['user_info']:
                user_info = auth_status['user_info']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Username", user_info.get('nickname', 'N/A'))
                with col2:
                    st.metric("Follower", user_info.get('follower_count', 0))
                with col3:
                    st.metric("Video", user_info.get('video_count', 0))
            
            # Pulsante logout
            if st.button("🚪 Logout"):
                self.oauth_client.logout()
                st.rerun()
            
            st.markdown("---")
            
            # Sezione import video
            self.render_import_section()
            
        else:
            st.warning("[ERROR] Non autenticato")
            
            # Configurazione OAuth
            with st.expander("[INFO] Configurazione OAuth"):
                st.info("""
                Per utilizzare il login TikTok, devi configurare le credenziali OAuth:
                
                1. Vai su [TikTok for Developers](https://developers.tiktok.com/)
                2. Crea una nuova app
                3. Configura le credenziali nel file `config/config.yaml`
                """)
                
                # Form per configurazione manuale
                client_key = st.text_input("Client Key", type="password")
                client_secret = st.text_input("Client Secret", type="password")
                
                if st.button("💾 Salva Configurazione"):
                    if client_key and client_secret:
                        self.save_oauth_config(client_key, client_secret)
                        st.success("Configurazione salvata!")
                        st.rerun()
                    else:
                        st.error("Inserisci entrambe le credenziali")
            
            # Login manuale con browser
            st.subheader("🌐 Login Manuale")
            st.info("""
            Se hai già configurato le credenziali OAuth, puoi procedere con il login manuale.
            Si aprirà una finestra del browser per completare l'autenticazione.
            """)
            
            if st.button("[INFO] Login con Browser"):
                self.start_manual_login()
    
    def render_import_section(self):
        """Renderizza sezione import video"""
        st.header("[INFO] Import Video")
        
        # Tab per diverse modalità
        tab1, tab2, tab3 = st.tabs(["🎯 Video Salvati", "[INFO] Collezioni", "[INFO] Link Manuali"])
        
        with tab1:
            self.render_saved_videos_tab()
        
        with tab2:
            self.render_collections_tab()
        
        with tab3:
            self.render_manual_links_tab()
    
    def render_saved_videos_tab(self):
        """Tab per video salvati"""
        st.subheader("🎯 Video Salvati")
        
        if st.button("[INFO] Importa Video Salvati", type="primary"):
            with st.spinner("Importazione video salvati in corso..."):
                self.import_saved_videos()
        
        # Mostra video importati
        if 'imported_videos' in st.session_state and st.session_state.imported_videos:
            st.subheader(f"[INFO] Video Importati ({len(st.session_state.imported_videos)})")
            
            for i, video in enumerate(st.session_state.imported_videos[:10]):  # Mostra primi 10
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if video.get('thumbnail'):
                            st.image(video['thumbnail'], width=120)
                        else:
                            st.image("https://via.placeholder.com/120x120?text=Video", width=120)
                    
                    with col2:
                        st.write(f"**Video {i+1}**")
                        if video.get('description'):
                            st.write(video['description'][:100] + "..." if len(video['description']) > 100 else video['description'])
                        if video.get('stats'):
                            st.write(f"[REPORT] {video['stats']}")
                        
                        # Pulsante per analisi
                        if st.button(f"[INFO] Analizza", key=f"analyze_{i}"):
                            self.analyze_video(video)
            
            if len(st.session_state.imported_videos) > 10:
                st.info(f"... e altri {len(st.session_state.imported_videos) - 10} video")
    
    def render_collections_tab(self):
        """Tab per collezioni"""
        st.subheader("[INFO] Collezioni")
        
        if st.button("[INFO] Importa Collezioni", type="primary"):
            with st.spinner("Importazione collezioni in corso..."):
                self.import_collections()
        
        # Mostra collezioni importate
        if 'imported_collections' in st.session_state and st.session_state.imported_collections:
            st.subheader(f"[INFO] Collezioni Importate ({len(st.session_state.imported_collections)})")
            
            for collection in st.session_state.imported_collections:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if collection.get('thumbnail'):
                            st.image(collection['thumbnail'], width=100)
                        else:
                            st.image("https://via.placeholder.com/100x100?text=Collection", width=100)
                    
                    with col2:
                        st.write(f"**{collection.get('name', 'Collezione')}**")
                        st.write(f"[INFO] {collection.get('video_count', 0)} video")
                        
                        if st.button(f"[INFO] Importa Video", key=f"import_collection_{collection.get('index', 0)}"):
                            self.import_collection_videos(collection)
    
    def render_manual_links_tab(self):
        """Tab per link manuali"""
        st.subheader("[INFO] Link Manuali")
        
        st.info("""
        Incolla qui i link dei video TikTok che vuoi analizzare.
        Puoi copiare i link dai tuoi video salvati su mobile.
        """)
        
        # Area testo per link
        links_text = st.text_area(
            "Link Video TikTok",
            height=200,
            placeholder="https://www.tiktok.com/@user/video/1234567890\nhttps://www.tiktok.com/@user/video/0987654321\n..."
        )
        
        if st.button("[INFO] Importa Link", type="primary"):
            if links_text.strip():
                self.import_manual_links(links_text)
            else:
                st.warning("Inserisci almeno un link")
    
    async def import_saved_videos(self):
        """Importa video salvati"""
        try:
            # Inizializza scraper
            self.scraper = TikTokSavesScraper(headless=True, slow_mo=100)
            
            async with self.scraper:
                # Login con sessione salvata
                session_file = Path("config/tiktok_session.json")
                if session_file.exists():
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if await self.scraper.login_with_session(session_data):
                        st.success("[OK] Login con sessione salvata")
                    else:
                        st.warning("[WARN]️ Sessione scaduta, login manuale richiesto")
                        if await self.scraper.manual_login():
                            st.success("[OK] Login manuale completato")
                        else:
                            st.error("[ERROR] Login fallito")
                            return
                else:
                    st.warning("[WARN]️ Nessuna sessione trovata, login manuale richiesto")
                    if await self.scraper.manual_login():
                        st.success("[OK] Login manuale completato")
                    else:
                        st.error("[ERROR] Login fallito")
                        return
                
                # Salva nuova sessione
                await self.scraper.save_session_data()
                
                # Importa video salvati
                videos = await self.scraper.get_saved_videos(max_videos=50)
                
                if videos:
                    st.session_state.imported_videos = videos
                    st.success(f"[OK] Importati {len(videos)} video salvati")
                else:
                    st.warning("[WARN]️ Nessun video salvato trovato")
        
        except Exception as e:
            st.error(f"[ERROR] Errore importazione: {e}")
            logger.error(f"Import error: {e}")
    
    async def import_collections(self):
        """Importa collezioni"""
        try:
            if not self.scraper:
                self.scraper = TikTokSavesScraper(headless=True, slow_mo=100)
            
            async with self.scraper:
                # Login (riusa logica precedente)
                session_file = Path("config/tiktok_session.json")
                if session_file.exists():
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if not await self.scraper.login_with_session(session_data):
                        if not await self.scraper.manual_login():
                            st.error("[ERROR] Login fallito")
                            return
                else:
                    if not await self.scraper.manual_login():
                        st.error("[ERROR] Login fallito")
                        return
                
                # Importa collezioni
                collections = await self.scraper.get_collections()
                
                if collections:
                    st.session_state.imported_collections = collections
                    st.success(f"[OK] Importate {len(collections)} collezioni")
                else:
                    st.warning("[WARN]️ Nessuna collezione trovata")
        
        except Exception as e:
            st.error(f"[ERROR] Errore importazione collezioni: {e}")
            logger.error(f"Collections import error: {e}")
    
    async def import_collection_videos(self, collection: Dict[str, Any]):
        """Importa video da una collezione specifica"""
        try:
            if not self.scraper:
                self.scraper = TikTokSavesScraper(headless=True, slow_mo=100)
            
            async with self.scraper:
                # Login (riusa logica precedente)
                session_file = Path("config/tiktok_session.json")
                if session_file.exists():
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if not await self.scraper.login_with_session(session_data):
                        if not await self.scraper.manual_login():
                            st.error("[ERROR] Login fallito")
                            return
                else:
                    if not await self.scraper.manual_login():
                        st.error("[ERROR] Login fallito")
                        return
                
                # Importa video dalla collezione
                videos = await self.scraper.get_collection_videos(
                    collection['url'], 
                    max_videos=50
                )
                
                if videos:
                    if 'imported_videos' not in st.session_state:
                        st.session_state.imported_videos = []
                    
                    st.session_state.imported_videos.extend(videos)
                    st.success(f"[OK] Importati {len(videos)} video dalla collezione '{collection.get('name', 'Collezione')}'")
                else:
                    st.warning("[WARN]️ Nessun video trovato nella collezione")
        
        except Exception as e:
            st.error(f"[ERROR] Errore importazione video collezione: {e}")
            logger.error(f"Collection videos import error: {e}")
    
    def import_manual_links(self, links_text: str):
        """Importa link manuali"""
        try:
            # Parsing link
            links = [link.strip() for link in links_text.split('\n') if link.strip()]
            valid_links = []
            
            for link in links:
                if 'tiktok.com' in link and '/video/' in link:
                    valid_links.append({
                        'url': link,
                        'description': f"Video importato manualmente",
                        'stats': "Import manuale",
                        'index': len(valid_links)
                    })
                else:
                    st.warning(f"[WARN]️ Link non valido: {link}")
            
            if valid_links:
                if 'imported_videos' not in st.session_state:
                    st.session_state.imported_videos = []
                
                st.session_state.imported_videos.extend(valid_links)
                st.success(f"[OK] Importati {len(valid_links)} link validi")
            else:
                st.warning("[WARN]️ Nessun link valido trovato")
        
        except Exception as e:
            st.error(f"[ERROR] Errore importazione link: {e}")
            logger.error(f"Manual links import error: {e}")
    
    def save_oauth_config(self, client_key: str, client_secret: str):
        """Salva configurazione OAuth"""
        try:
            config_file = Path("config/config.yaml")
            config_file.parent.mkdir(exist_ok=True)
            
            import yaml
            
            # Carica configurazione esistente
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            else:
                config = {}
            
            # Aggiorna configurazione TikTok
            if 'tiktok' not in config:
                config['tiktok'] = {}
            
            config['tiktok']['client_key'] = client_key
            config['tiktok']['client_secret'] = client_secret
            config['tiktok']['redirect_uri'] = 'http://localhost:8501/auth/callback'
            config['tiktok']['scope'] = 'user.info.basic,video.list'
            
            # Salva configurazione
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            
            logger.info("OAuth configuration saved")
        
        except Exception as e:
            logger.error(f"Failed to save OAuth config: {e}")
            raise
    
    def start_manual_login(self):
        """Avvia login manuale"""
        st.info("[INFO] Avvio login manuale...")
        st.info("Si aprirà una finestra del browser. Completa il login e torna qui.")
        
        # Qui potresti implementare la logica per aprire il browser
        # Per ora, mostra istruzioni
        st.markdown("""
        ### [INFO] Istruzioni Login Manuale:
        
        1. **Apri il browser** e vai su [TikTok Login](https://www.tiktok.com/login)
        2. **Completa il login** con le tue credenziali
        3. **Torna qui** e clicca su "Verifica Login"
        4. **Importa i video** salvati
        """)
    
    def analyze_video(self, video: Dict[str, Any]):
        """Analizza un singolo video"""
        st.info(f"[INFO] Analisi video: {video.get('url', 'N/A')}")
        # Qui implementa la logica di analisi video
        # Puoi integrare con il pipeline di analisi esistente
    
    def run(self):
        """Esegui l'interfaccia"""
        self.render_sidebar()
        self.render_login_section()

def main():
    """Funzione principale"""
    interface = TikTokImportInterface()
    interface.run()

if __name__ == "__main__":
    main() 