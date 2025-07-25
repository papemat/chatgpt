#!/usr/bin/env python3
"""
TokIntel v2 - TikTok Video Downloader Module
Download automatico e salvataggio video TikTok con cache locale
"""

import asyncio
import logging
import json
import time
import os
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re
import aiohttp
import aiofiles
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available. Install with: pip install playwright")

class TikTokVideoDownloader:
    """Downloader per video TikTok con cache locale"""
    
    def __init__(self, cache_dir: str = "cache/videos", headless: bool = True):
        """
        Inizializza il downloader
        
        Args:
            cache_dir: Directory per la cache dei video
            headless: Esegui browser in modalità headless
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        self.browser = None
        self.page = None
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright is required. Install with: pip install playwright")
        
        logger.info(f"TikTok video downloader initialized with cache: {self.cache_dir}")
    
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
            
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
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
    
    def get_video_id_from_url(self, url: str) -> Optional[str]:
        """Estrae l'ID del video dall'URL TikTok"""
        try:
            # Pattern per URL TikTok
            patterns = [
                r'tiktok\.com/@[\w.-]+/video/(\d+)',
                r'tiktok\.com/v/(\d+)',
                r'tiktok\.com/t/(\w+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
        except Exception as e:
            logger.error(f"Error extracting video ID: {e}")
            return None
    
    def get_cache_path(self, video_id: str) -> Path:
        """Genera il percorso della cache per un video"""
        return self.cache_dir / f"{video_id}.mp4"
    
    def get_metadata_path(self, video_id: str) -> Path:
        """Genera il percorso per i metadati del video"""
        return self.cache_dir / f"{video_id}_metadata.json"
    
    def is_video_cached(self, video_id: str) -> bool:
        """Verifica se un video è già in cache"""
        video_path = self.get_cache_path(video_id)
        metadata_path = self.get_metadata_path(video_id)
        return video_path.exists() and metadata_path.exists()
    
    async def get_video_download_url(self, tiktok_url: str) -> Optional[str]:
        """Ottiene l'URL di download diretto del video"""
        try:
            await self.page.goto(tiktok_url, wait_until='networkidle')
            await asyncio.sleep(2)
            
            # Aspetta che il video sia caricato
            await self.page.wait_for_selector('video', timeout=10000)
            
            # Cerca l'elemento video e ottieni il src
            video_element = await self.page.query_selector('video')
            if video_element:
                video_src = await video_element.get_attribute('src')
                if video_src:
                    return video_src
            
            # Alternativa: cerca nei network requests
            async for request in self.page.request.all():
                if 'video' in request.url and request.url.endswith('.mp4'):
                    return request.url
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting video download URL: {e}")
            return None
    
    async def download_video(self, video_url: str, video_id: str) -> bool:
        """Scarica il video e lo salva in cache"""
        try:
            download_url = await self.get_video_download_url(video_url)
            if not download_url:
                logger.error(f"Could not get download URL for video {video_id}")
                return False
            
            # Scarica il video
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        video_path = self.get_cache_path(video_id)
                        async with aiofiles.open(video_path, 'wb') as f:
                            await f.write(await response.read())
                        
                        logger.info(f"Video downloaded successfully: {video_path}")
                        return True
                    else:
                        logger.error(f"Failed to download video: HTTP {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error downloading video {video_id}: {e}")
            return False
    
    async def save_video_metadata(self, video_id: str, metadata: Dict[str, Any]) -> bool:
        """Salva i metadati del video"""
        try:
            metadata_path = self.get_metadata_path(video_id)
            metadata['downloaded_at'] = datetime.utcnow().isoformat()
            metadata['video_id'] = video_id
            
            async with aiofiles.open(metadata_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(metadata, indent=2, ensure_ascii=False))
            
            logger.info(f"Metadata saved: {metadata_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            return False
    
    async def get_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Carica i metadati del video dalla cache"""
        try:
            metadata_path = self.get_metadata_path(video_id)
            if metadata_path.exists():
                async with aiofiles.open(metadata_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    return json.loads(content)
            return None
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            return None
    
    async def download_video_with_metadata(self, tiktok_url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Download completo di video e metadati
        
        Returns:
            Dict con status, video_id, file_path, metadata
        """
        video_id = self.get_video_id_from_url(tiktok_url)
        if not video_id:
            return {
                'success': False,
                'error': 'Could not extract video ID from URL'
            }
        
        # Verifica se già in cache
        if self.is_video_cached(video_id):
            cached_metadata = await self.get_video_metadata(video_id)
            return {
                'success': True,
                'video_id': video_id,
                'file_path': str(self.get_cache_path(video_id)),
                'metadata': cached_metadata,
                'cached': True
            }
        
        # Download del video
        download_success = await self.download_video(tiktok_url, video_id)
        if not download_success:
            return {
                'success': False,
                'video_id': video_id,
                'error': 'Failed to download video'
            }
        
        # Salva metadati
        if metadata:
            await self.save_video_metadata(video_id, metadata)
        
        return {
            'success': True,
            'video_id': video_id,
            'file_path': str(self.get_cache_path(video_id)),
            'metadata': metadata,
            'cached': False
        }
    
    async def batch_download_videos(self, video_urls: List[str], metadata_list: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Download batch di video"""
        results = []
        
        for i, url in enumerate(video_urls):
            metadata = metadata_list[i] if metadata_list and i < len(metadata_list) else None
            result = await self.download_video_with_metadata(url, metadata)
            results.append(result)
            
            # Pausa tra download per evitare rate limiting
            await asyncio.sleep(1)
        
        return results
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Ottiene statistiche della cache"""
        try:
            video_files = list(self.cache_dir.glob("*.mp4"))
            metadata_files = list(self.cache_dir.glob("*_metadata.json"))
            
            total_size = sum(f.stat().st_size for f in video_files)
            
            return {
                'total_videos': len(video_files),
                'total_metadata': len(metadata_files),
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'cache_dir': str(self.cache_dir)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def clear_cache(self, video_id: str = None) -> bool:
        """Pulisce la cache (tutto o video specifico)"""
        try:
            if video_id:
                # Rimuovi video specifico
                video_path = self.get_cache_path(video_id)
                metadata_path = self.get_metadata_path(video_id)
                
                if video_path.exists():
                    video_path.unlink()
                if metadata_path.exists():
                    metadata_path.unlink()
                
                logger.info(f"Cleared cache for video {video_id}")
            else:
                # Rimuovi tutto
                for file_path in self.cache_dir.glob("*"):
                    file_path.unlink()
                logger.info("Cleared entire cache")
            
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

# Funzioni di utilità per integrazione con il sistema esistente
async def download_video_for_analysis(tiktok_url: str, user_id: int = 1) -> Dict[str, Any]:
    """
    Download video per analisi - integrazione con sistema esistente
    
    Args:
        tiktok_url: URL del video TikTok
        user_id: ID utente per associare il download
    
    Returns:
        Dict con risultati del download
    """
    async with TikTokVideoDownloader() as downloader:
        # Metadati base per il video
        metadata = {
            'user_id': user_id,
            'original_url': tiktok_url,
            'download_timestamp': datetime.utcnow().isoformat(),
            'analysis_ready': True
        }
        
        result = await downloader.download_video_with_metadata(tiktok_url, metadata)
        
        # Log dell'evento
        logger.info(f"Video download for user {user_id}: {result}")
        
        return result

async def get_user_cached_videos(user_id: int) -> List[Dict[str, Any]]:
    """
    Ottiene tutti i video in cache per un utente specifico
    
    Args:
        user_id: ID utente
    
    Returns:
        Lista di video con metadati
    """
    downloader = TikTokVideoDownloader()
    cached_videos = []
    
    try:
        # Cerca tutti i file di metadati
        metadata_files = list(downloader.cache_dir.glob("*_metadata.json"))
        
        for metadata_file in metadata_files:
            try:
                async with aiofiles.open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.loads(await f.read())
                
                # Filtra per utente
                if metadata.get('user_id') == user_id:
                    video_id = metadata.get('video_id')
                    video_path = downloader.get_cache_path(video_id)
                    
                    if video_path.exists():
                        cached_videos.append({
                            'video_id': video_id,
                            'file_path': str(video_path),
                            'metadata': metadata,
                            'file_size_mb': round(video_path.stat().st_size / (1024 * 1024), 2)
                        })
            except Exception as e:
                logger.error(f"Error reading metadata file {metadata_file}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error getting cached videos: {e}")
    
    return cached_videos

if __name__ == "__main__":
    # Test del downloader
    async def test_download():
        test_url = "https://www.tiktok.com/@username/video/1234567890123456789"
        
        async with TikTokVideoDownloader(headless=False) as downloader:
            result = await downloader.download_video_with_metadata(test_url)
            print(f"Download result: {result}")
            
            stats = downloader.get_cache_stats()
            print(f"Cache stats: {stats}")
    
    asyncio.run(test_download()) 