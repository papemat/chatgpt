#!/usr/bin/env python3
"""
TokIntel v2 - TikTok Saves Scraper Module
Estrazione video salvati e collezioni tramite browser headless
"""

import asyncio
import logging
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re

logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available. Install with: pip install playwright")

class TikTokSavesScraper:
    """Scraper per video salvati TikTok usando browser headless"""
    
    def __init__(self, headless: bool = True, slow_mo: int = 100):
        """
        Inizializza lo scraper
        
        Args:
            headless: Esegui browser in modalità headless
            slow_mo: Ritardo tra azioni (ms)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser = None
        self.page = None
        self.is_logged_in = False
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright is required. Install with: pip install playwright")
        
        logger.info("TikTok saves scraper initialized")
    
    async def __aenter__(self):
        """Context manager entry"""
        await self.start_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close_browser()
    
    async def start_browser(self):
        """Avvia browser Playwright"""
        try:
            self.playwright = await async_playwright().start()
            
            # Usa Chromium per migliore compatibilità
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            # Crea nuova pagina
            self.page = await self.browser.new_page()
            
            # Imposta user agent realistico
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            logger.info("Browser started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    async def close_browser(self):
        """Chiudi browser e pulisci risorse"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            
            logger.info("Browser closed")
            
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def login_with_session(self, session_data: Dict[str, Any]) -> bool:
        """
        Login usando dati sessione salvati
        
        Args:
            session_data: Dati sessione TikTok
            
        Returns:
            bool: True se login riuscito
        """
        try:
            # Vai alla pagina TikTok
            await self.page.goto('https://www.tiktok.com/', wait_until='networkidle')
            
            # Inietta cookies di sessione
            cookies = session_data.get('cookies', [])
            if cookies:
                await self.page.context.add_cookies(cookies)
                logger.info(f"Injected {len(cookies)} cookies")
            
            # Verifica se già loggato
            await self.page.wait_for_timeout(2000)
            
            # Controlla se c'è il pulsante login
            login_button = await self.page.query_selector('[data-e2e="login-button"]')
            if not login_button:
                logger.info("Already logged in")
                self.is_logged_in = True
                return True
            
            # Se non loggato, prova con localStorage
            local_storage = session_data.get('localStorage', {})
            if local_storage:
                await self.page.evaluate("""
                    (storage) => {
                        for (const [key, value] of Object.entries(storage)) {
                            localStorage.setItem(key, value);
                        }
                    }
                """, local_storage)
                
                # Ricarica pagina
                await self.page.reload(wait_until='networkidle')
                await self.page.wait_for_timeout(3000)
                
                # Verifica di nuovo
                login_button = await self.page.query_selector('[data-e2e="login-button"]')
                if not login_button:
                    logger.info("Login successful via localStorage")
                    self.is_logged_in = True
                    return True
            
            logger.warning("Could not login with session data")
            return False
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def manual_login(self) -> bool:
        """
        Login manuale interattivo
        
        Returns:
            bool: True se login riuscito
        """
        try:
            # Vai alla pagina login TikTok
            await self.page.goto('https://www.tiktok.com/login', wait_until='networkidle')
            
            logger.info("Manual login required. Please login in the browser window.")
            logger.info("Waiting for user to complete login...")
            
            # Aspetta che l'utente faccia login
            # Controlla se il pulsante login scompare
            max_wait = 300  # 5 minuti
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                login_button = await self.page.query_selector('[data-e2e="login-button"]')
                if not login_button:
                    # Verifica se siamo nella pagina principale
                    current_url = self.page.url
                    if 'tiktok.com' in current_url and 'login' not in current_url:
                        logger.info("Manual login completed successfully")
                        self.is_logged_in = True
                        return True
                
                await asyncio.sleep(2)
            
            logger.error("Manual login timeout")
            return False
            
        except Exception as e:
            logger.error(f"Manual login failed: {e}")
            return False
    
    async def get_saved_videos(self, max_videos: int = 50) -> List[Dict[str, Any]]:
        """
        Estrae video salvati dall'account
        
        Args:
            max_videos: Numero massimo di video da estrarre
            
        Returns:
            Lista di video salvati
        """
        if not self.is_logged_in:
            raise ValueError("Not logged in. Call login_with_session() or manual_login() first")
        
        try:
            # Vai alla pagina video salvati
            await self.page.goto('https://www.tiktok.com/favorites', wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            videos = []
            last_height = 0
            
            while len(videos) < max_videos:
                # Estrai video dalla pagina corrente
                page_videos = await self._extract_videos_from_page()
                
                for video in page_videos:
                    if video not in videos:
                        videos.append(video)
                        if len(videos) >= max_videos:
                            break
                
                # Scroll per caricare più video
                current_height = await self.page.evaluate('document.body.scrollHeight')
                if current_height == last_height:
                    # Non ci sono più video da caricare
                    break
                
                await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await self.page.wait_for_timeout(2000)
                last_height = current_height
            
            logger.info(f"Extracted {len(videos)} saved videos")
            return videos
            
        except Exception as e:
            logger.error(f"Failed to get saved videos: {e}")
            return []
    
    async def get_collections(self) -> List[Dict[str, Any]]:
        """
        Estrae collezioni dell'utente
        
        Returns:
            Lista di collezioni
        """
        if not self.is_logged_in:
            raise ValueError("Not logged in")
        
        try:
            # Vai alla pagina collezioni
            await self.page.goto('https://www.tiktok.com/collections', wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            collections = await self._extract_collections_from_page()
            logger.info(f"Extracted {len(collections)} collections")
            return collections
            
        except Exception as e:
            logger.error(f"Failed to get collections: {e}")
            return []
    
    async def get_collection_videos(self, collection_url: str, max_videos: int = 50) -> List[Dict[str, Any]]:
        """
        Estrae video da una collezione specifica
        
        Args:
            collection_url: URL della collezione
            max_videos: Numero massimo di video
            
        Returns:
            Lista di video nella collezione
        """
        if not self.is_logged_in:
            raise ValueError("Not logged in")
        
        try:
            await self.page.goto(collection_url, wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            videos = []
            last_height = 0
            
            while len(videos) < max_videos:
                page_videos = await self._extract_videos_from_page()
                
                for video in page_videos:
                    if video not in videos:
                        videos.append(video)
                        if len(videos) >= max_videos:
                            break
                
                # Scroll per caricare più video
                current_height = await self.page.evaluate('document.body.scrollHeight')
                if current_height == last_height:
                    break
                
                await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await self.page.wait_for_timeout(2000)
                last_height = current_height
            
            logger.info(f"Extracted {len(videos)} videos from collection")
            return videos
            
        except Exception as e:
            logger.error(f"Failed to get collection videos: {e}")
            return []
    
    async def _extract_videos_from_page(self) -> List[Dict[str, Any]]:
        """Estrae video dalla pagina corrente"""
        try:
            videos = await self.page.evaluate("""
                () => {
                    const videos = [];
                    const videoElements = document.querySelectorAll('[data-e2e="user-post-item"]');
                    
                    videoElements.forEach((element, index) => {
                        try {
                            // Estrai link del video
                            const linkElement = element.querySelector('a[href*="/video/"]');
                            const videoUrl = linkElement ? linkElement.href : null;
                            
                            // Estrai thumbnail
                            const imgElement = element.querySelector('img');
                            const thumbnail = imgElement ? imgElement.src : null;
                            
                            // Estrai testo descrizione
                            const textElement = element.querySelector('[data-e2e="user-post-item-desc"]');
                            const description = textElement ? textElement.textContent : '';
                            
                            // Estrai statistiche
                            const statsElement = element.querySelector('[data-e2e="user-post-item-stats"]');
                            const stats = statsElement ? statsElement.textContent : '';
                            
                            if (videoUrl) {
                                videos.push({
                                    url: videoUrl,
                                    thumbnail: thumbnail,
                                    description: description,
                                    stats: stats,
                                    index: index
                                });
                            }
                        } catch (e) {
                            console.error('Error extracting video:', e);
                        }
                    });
                    
                    return videos;
                }
            """)
            
            return videos
            
        except Exception as e:
            logger.error(f"Error extracting videos from page: {e}")
            return []
    
    async def _extract_collections_from_page(self) -> List[Dict[str, Any]]:
        """Estrae collezioni dalla pagina corrente"""
        try:
            collections = await self.page.evaluate("""
                () => {
                    const collections = [];
                    const collectionElements = document.querySelectorAll('[data-e2e="collection-item"]');
                    
                    collectionElements.forEach((element, index) => {
                        try {
                            // Estrai link della collezione
                            const linkElement = element.querySelector('a');
                            const collectionUrl = linkElement ? linkElement.href : null;
                            
                            // Estrai nome collezione
                            const nameElement = element.querySelector('[data-e2e="collection-name"]');
                            const name = nameElement ? nameElement.textContent : '';
                            
                            // Estrai numero video
                            const countElement = element.querySelector('[data-e2e="collection-count"]');
                            const videoCount = countElement ? countElement.textContent : '';
                            
                            // Estrai thumbnail
                            const imgElement = element.querySelector('img');
                            const thumbnail = imgElement ? imgElement.src : null;
                            
                            if (collectionUrl) {
                                collections.push({
                                    url: collectionUrl,
                                    name: name,
                                    video_count: videoCount,
                                    thumbnail: thumbnail,
                                    index: index
                                });
                            }
                        } catch (e) {
                            console.error('Error extracting collection:', e);
                        }
                    });
                    
                    return collections;
                }
            """)
            
            return collections
            
        except Exception as e:
            logger.error(f"Error extracting collections from page: {e}")
            return []
    
    async def save_session_data(self, file_path: str = "config/tiktok_session.json"):
        """Salva dati sessione per riutilizzo futuro"""
        try:
            # Estrai cookies
            cookies = await self.page.context.cookies()
            
            # Estrai localStorage
            local_storage = await self.page.evaluate("""
                () => {
                    const storage = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        storage[key] = localStorage.getItem(key);
                    }
                    return storage;
                }
            """)
            
            session_data = {
                'cookies': cookies,
                'localStorage': local_storage,
                'timestamp': time.time()
            }
            
            # Salva su file
            Path(file_path).parent.mkdir(exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Session data saved to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save session data: {e}")
    
    def extract_video_id_from_url(self, url: str) -> Optional[str]:
        """Estrae ID video da URL TikTok"""
        try:
            # Pattern per URL TikTok video
            patterns = [
                r'/video/(\d+)',
                r'/v/(\d+)',
                r'tiktok\.com/@[^/]+/video/(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting video ID: {e}")
            return None 