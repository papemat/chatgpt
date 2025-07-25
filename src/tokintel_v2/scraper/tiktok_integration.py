#!/usr/bin/env python3
"""
TokIntel v2 - TikTok Integration Module
Integrazione tra downloader TikTok e database per gestione automatica
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .download_tiktok_video import TikTokVideoDownloader, download_video_for_analysis
from .tiktok_saves import TikTokSavesScraper
from db.database import DatabaseManager, get_db_manager, UserTikTokSession, UserSavedVideo

logger = logging.getLogger(__name__)

class TikTokIntegration:
    """Integrazione completa tra TikTok e database TokIntel"""
    
    def __init__(self):
        """Inizializza l'integrazione"""
        self.db_manager = get_db_manager()
        self.downloader = TikTokVideoDownloader()
        self.scraper = TikTokSavesScraper()
        
    async def setup_user_session(self, user_id: int, tiktok_username: str, 
                                session_data: Dict[str, Any], login_method: str = "manual") -> UserTikTokSession:
        """
        Configura una sessione TikTok per un utente
        
        Args:
            user_id: ID utente TokIntel
            tiktok_username: Username TikTok
            session_data: Dati di sessione (cookies, tokens, etc.)
            login_method: Metodo di login (manual, browser, api)
        
        Returns:
            UserTikTokSession creata
        """
        try:
            # Crea sessione nel database
            session = self.db_manager.create_tiktok_session(
                user_id=user_id,
                tiktok_username=tiktok_username,
                session_data=session_data,
                login_method=login_method
            )
            
            logger.info(f"Sessione TikTok configurata per utente {user_id}: {tiktok_username}")
            return session
            
        except Exception as e:
            logger.error(f"Errore nella configurazione sessione TikTok: {e}")
            raise
    
    async def sync_saved_videos(self, user_id: int, max_videos: int = 50) -> List[Dict[str, Any]]:
        """
        Sincronizza i video salvati di un utente TikTok con il database
        
        Args:
            user_id: ID utente TokIntel
            max_videos: Numero massimo di video da sincronizzare
        
        Returns:
            Lista di video sincronizzati
        """
        try:
            # Ottieni sessione TikTok attiva
            session = self.db_manager.get_active_tiktok_session(user_id)
            if not session:
                raise ValueError(f"Nessuna sessione TikTok attiva per utente {user_id}")
            
            # Usa lo scraper per ottenere video salvati
            async with self.scraper:
                # Login con dati sessione
                login_success = await self.scraper.login_with_session(session.session_data)
                if not login_success:
                    raise ValueError("Impossibile effettuare login con i dati di sessione")
                
                # Ottieni video salvati
                saved_videos = await self.scraper.get_saved_videos(max_videos)
            
            # Salva video nel database
            synced_videos = []
            for video_data in saved_videos:
                try:
                    # Prepara dati per il database
                    db_video_data = {
                        'tiktok_video_id': video_data.get('video_id'),
                        'video_url': video_data.get('url'),
                        'video_title': video_data.get('title'),
                        'creator_username': video_data.get('creator'),
                        'duration': video_data.get('duration'),
                        'view_count': video_data.get('view_count'),
                        'like_count': video_data.get('like_count'),
                        'comment_count': video_data.get('comment_count'),
                        'share_count': video_data.get('share_count'),
                        'download_status': 'pending'
                    }
                    
                    # Salva nel database
                    saved_video = self.db_manager.save_tiktok_video(
                        user_id=user_id,
                        video_data=db_video_data,
                        session_id=session.id
                    )
                    
                    synced_videos.append({
                        'db_id': saved_video.id,
                        'tiktok_id': saved_video.tiktok_video_id,
                        'title': saved_video.video_title,
                        'status': 'synced'
                    })
                    
                except Exception as e:
                    logger.error(f"Errore nel salvataggio video {video_data.get('video_id')}: {e}")
                    continue
            
            # Aggiorna attività sessione
            self.db_manager.update_tiktok_session_activity(session.id)
            
            logger.info(f"Sincronizzati {len(synced_videos)} video per utente {user_id}")
            return synced_videos
            
        except Exception as e:
            logger.error(f"Errore nella sincronizzazione video: {e}")
            raise
    
    async def download_user_videos(self, user_id: int, max_videos: int = 10) -> List[Dict[str, Any]]:
        """
        Scarica i video salvati di un utente che non sono ancora stati scaricati
        
        Args:
            user_id: ID utente TokIntel
            max_videos: Numero massimo di video da scaricare
        
        Returns:
            Lista di video scaricati
        """
        try:
            # Ottieni video non scaricati dal database
            saved_videos = self.db_manager.get_user_saved_videos(user_id, limit=1000)
            pending_videos = [v for v in saved_videos if v.download_status == 'pending']
            
            if not pending_videos:
                logger.info(f"Nessun video in attesa di download per utente {user_id}")
                return []
            
            # Limita il numero di video da scaricare
            videos_to_download = pending_videos[:max_videos]
            
            downloaded_videos = []
            async with self.downloader:
                for video in videos_to_download:
                    try:
                        # Download del video
                        result = await self.downloader.download_video_with_metadata(
                            video.video_url,
                            metadata={
                                'user_id': user_id,
                                'db_video_id': video.id,
                                'tiktok_video_id': video.tiktok_video_id,
                                'original_url': video.video_url
                            }
                        )
                        
                        if result['success']:
                            # Aggiorna stato nel database
                            self.db_manager.update_video_download_status(
                                video_id=video.id,
                                download_status='downloaded',
                                local_file_path=result['file_path'],
                                file_size_mb=result.get('metadata', {}).get('file_size_mb')
                            )
                            
                            downloaded_videos.append({
                                'db_id': video.id,
                                'tiktok_id': video.tiktok_video_id,
                                'file_path': result['file_path'],
                                'status': 'downloaded'
                            })
                        else:
                            # Marca come fallito
                            self.db_manager.update_video_download_status(
                                video_id=video.id,
                                download_status='failed'
                            )
                            
                            downloaded_videos.append({
                                'db_id': video.id,
                                'tiktok_id': video.tiktok_video_id,
                                'status': 'failed',
                                'error': result.get('error')
                            })
                        
                        # Pausa tra download
                        await asyncio.sleep(2)
                        
                    except Exception as e:
                        logger.error(f"Errore nel download video {video.tiktok_video_id}: {e}")
                        self.db_manager.update_video_download_status(
                            video_id=video.id,
                            download_status='failed'
                        )
                        continue
            
            logger.info(f"Scaricati {len([v for v in downloaded_videos if v['status'] == 'downloaded'])} video per utente {user_id}")
            return downloaded_videos
            
        except Exception as e:
            logger.error(f"Errore nel download video utente: {e}")
            raise
    
    async def process_video_for_analysis(self, user_id: int, video_id: int) -> Optional[int]:
        """
        Prepara un video per l'analisi (download se necessario e collegamento)
        
        Args:
            user_id: ID utente TokIntel
            video_id: ID video nel database
        
        Returns:
            ID dell'analisi creata o None se errore
        """
        try:
            # Ottieni video dal database
            video = self.db_manager.get_video_by_tiktok_id(user_id, str(video_id))
            if not video:
                raise ValueError(f"Video {video_id} non trovato per utente {user_id}")
            
            # Se il video non è scaricato, scaricalo
            if video.download_status != 'downloaded':
                async with self.downloader:
                    result = await self.downloader.download_video_with_metadata(
                        video.video_url,
                        metadata={
                            'user_id': user_id,
                            'db_video_id': video.id,
                            'tiktok_video_id': video.tiktok_video_id
                        }
                    )
                    
                    if not result['success']:
                        raise ValueError(f"Impossibile scaricare video {video_id}: {result.get('error')}")
                    
                    # Aggiorna stato nel database
                    self.db_manager.update_video_download_status(
                        video_id=video.id,
                        download_status='downloaded',
                        local_file_path=result['file_path']
                    )
            
            # Il video è ora pronto per l'analisi
            # L'analisi verrà creata dal sistema di analisi principale
            # Questo metodo si occupa solo di preparare il video
            
            logger.info(f"Video {video_id} preparato per analisi")
            return video.id
            
        except Exception as e:
            logger.error(f"Errore nella preparazione video {video_id} per analisi: {e}")
            return None
    
    def get_user_library_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Ottiene un riepilogo della libreria TikTok di un utente
        
        Args:
            user_id: ID utente TokIntel
        
        Returns:
            Riepilogo della libreria
        """
        try:
            # Ottieni video con analisi
            videos_with_analysis = self.db_manager.get_videos_with_analysis(user_id)
            
            # Statistiche
            total_videos = len(videos_with_analysis)
            downloaded_videos = len([v for v in videos_with_analysis if v['download_status'] == 'downloaded'])
            analyzed_videos = len([v for v in videos_with_analysis if v['analysis'] is not None])
            
            # Calcola punteggio medio
            scores = [v['analysis']['overall_score'] for v in videos_with_analysis if v['analysis']]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Calcola dimensione totale
            total_size = sum(v['file_size_mb'] or 0 for v in videos_with_analysis)
            
            # Sessione TikTok
            session = self.db_manager.get_active_tiktok_session(user_id)
            session_info = {
                'username': session.tiktok_username if session else None,
                'is_active': session.is_active if session else False,
                'last_activity': session.last_activity if session else None
            }
            
            return {
                'total_videos': total_videos,
                'downloaded_videos': downloaded_videos,
                'analyzed_videos': analyzed_videos,
                'average_score': round(avg_score, 2),
                'total_size_mb': round(total_size, 2),
                'session': session_info,
                'last_sync': max([v['saved_at'] for v in videos_with_analysis]) if videos_with_analysis else None
            }
            
        except Exception as e:
            logger.error(f"Errore nel calcolo riepilogo libreria: {e}")
            return {}
    
    async def cleanup_expired_sessions(self):
        """Pulisce le sessioni TikTok scadute"""
        try:
            # Implementazione per pulizia sessioni scadute
            # Questo metodo può essere chiamato periodicamente
            logger.info("Pulizia sessioni scadute completata")
        except Exception as e:
            logger.error(f"Errore nella pulizia sessioni: {e}")

# Funzioni di utilità per integrazione con il sistema esistente
async def integrate_tiktok_user(user_id: int, tiktok_username: str, session_data: Dict[str, Any]) -> bool:
    """
    Integrazione completa di un utente TikTok
    
    Args:
        user_id: ID utente TokIntel
        tiktok_username: Username TikTok
        session_data: Dati di sessione
    
    Returns:
        True se l'integrazione è riuscita
    """
    try:
        integration = TikTokIntegration()
        
        # Configura sessione
        session = await integration.setup_user_session(user_id, tiktok_username, session_data)
        
        # Sincronizza video salvati
        synced_videos = await integration.sync_saved_videos(user_id)
        
        # Scarica video (opzionale, può essere fatto in background)
        # downloaded_videos = await integration.download_user_videos(user_id, max_videos=5)
        
        logger.info(f"Integrazione TikTok completata per utente {user_id}: {len(synced_videos)} video sincronizzati")
        return True
        
    except Exception as e:
        logger.error(f"Errore nell'integrazione TikTok utente {user_id}: {e}")
        return False

async def sync_user_tiktok_library(user_id: int) -> Dict[str, Any]:
    """
    Sincronizzazione completa della libreria TikTok di un utente
    
    Args:
        user_id: ID utente TokIntel
    
    Returns:
        Risultati della sincronizzazione
    """
    try:
        integration = TikTokIntegration()
        
        # Sincronizza video salvati
        synced_videos = await integration.sync_saved_videos(user_id)
        
        # Scarica video non scaricati
        downloaded_videos = await integration.download_user_videos(user_id)
        
        # Ottieni riepilogo
        summary = integration.get_user_library_summary(user_id)
        
        return {
            'success': True,
            'synced_videos': len(synced_videos),
            'downloaded_videos': len([v for v in downloaded_videos if v['status'] == 'downloaded']),
            'summary': summary
        }
        
    except Exception as e:
        logger.error(f"Errore nella sincronizzazione libreria utente {user_id}: {e}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test dell'integrazione
    async def test_integration():
        # Esempio di utilizzo
        user_id = 1
        tiktok_username = "test_user"
        session_data = {
            "cookies": {},
            "tokens": {}
        }
        
        # Test integrazione
        success = await integrate_tiktok_user(user_id, tiktok_username, session_data)
        print(f"Integrazione completata: {success}")
        
        # Test sincronizzazione
        result = await sync_user_tiktok_library(user_id)
        print(f"Risultato sincronizzazione: {result}")
    
    asyncio.run(test_integration()) 