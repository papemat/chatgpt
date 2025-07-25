#!/usr/bin/env python3
"""
Test per le funzionalità della libreria TikTok
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from scraper.download_tiktok_video import TikTokVideoDownloader, download_video_for_analysis, get_user_cached_videos
from scraper.tiktok_integration import TikTokIntegration, integrate_tiktok_user, sync_user_tiktok_library
from db.database import DatabaseManager, UserTikTokSession, UserSavedVideo

class TestTikTokVideoDownloader:
    """Test per il downloader video TikTok"""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Crea una directory temporanea per i test"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def downloader(self, temp_cache_dir):
        """Crea un'istanza del downloader per i test"""
        return TikTokVideoDownloader(cache_dir=temp_cache_dir)
    
    def test_get_video_id_from_url(self, downloader):
        """Test estrazione ID video da URL"""
        test_urls = [
            "https://www.tiktok.com/@username/video/1234567890123456789",
            "https://www.tiktok.com/v/1234567890123456789",
            "https://www.tiktok.com/t/abc123"
        ]
        
        expected_ids = [
            "1234567890123456789",
            "1234567890123456789", 
            "abc123"
        ]
        
        for url, expected_id in zip(test_urls, expected_ids):
            video_id = downloader.get_video_id_from_url(url)
            assert video_id == expected_id
    
    def test_get_cache_path(self, downloader):
        """Test generazione percorso cache"""
        video_id = "1234567890123456789"
        cache_path = downloader.get_cache_path(video_id)
        metadata_path = downloader.get_metadata_path(video_id)
        
        assert str(cache_path).endswith("1234567890123456789.mp4")
        assert str(metadata_path).endswith("1234567890123456789_metadata.json")
    
    def test_is_video_cached(self, downloader, temp_cache_dir):
        """Test verifica video in cache"""
        video_id = "1234567890123456789"
        
        # Video non in cache
        assert not downloader.is_video_cached(video_id)
        
        # Crea file video e metadati
        video_path = downloader.get_cache_path(video_id)
        metadata_path = downloader.get_metadata_path(video_id)
        
        video_path.touch()
        metadata_path.touch()
        
        # Video ora in cache
        assert downloader.is_video_cached(video_id)
    
    @pytest.mark.asyncio
    async def test_download_video_with_metadata(self, downloader):
        """Test download video con metadati"""
        # Mock del browser e download
        with patch.object(downloader, 'start_browser'), \
             patch.object(downloader, 'close_browser'), \
             patch.object(downloader, 'get_video_download_url', return_value="http://example.com/video.mp4"), \
             patch('aiohttp.ClientSession') as mock_session:
            
            # Mock della risposta HTTP
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read = AsyncMock(return_value=b"fake video data")
            
            mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
            
            # Test download
            result = await downloader.download_video_with_metadata(
                "https://www.tiktok.com/@username/video/1234567890123456789",
                metadata={'user_id': 1, 'test': True}
            )
            
            assert result['success'] is True
            assert 'video_id' in result
            assert result['cached'] is False
    
    def test_get_cache_stats(self, downloader, temp_cache_dir):
        """Test statistiche cache"""
        # Crea alcuni file di test
        video_files = [
            "1234567890123456789.mp4",
            "9876543210987654321.mp4"
        ]
        metadata_files = [
            "1234567890123456789_metadata.json",
            "9876543210987654321_metadata.json"
        ]
        
        for video_file in video_files:
            (Path(temp_cache_dir) / video_file).touch()
        
        for metadata_file in metadata_files:
            (Path(temp_cache_dir) / metadata_file).touch()
        
        stats = downloader.get_cache_stats()
        
        assert stats['total_videos'] == 2
        assert stats['total_metadata'] == 2
        assert 'total_size_mb' in stats

class TestTikTokIntegration:
    """Test per l'integrazione TikTok"""
    
    @pytest.fixture
    def integration(self):
        """Crea un'istanza dell'integrazione per i test"""
        return TikTokIntegration()
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock del database manager"""
        with patch('scraper.tiktok_integration.get_db_manager') as mock:
            db_manager = Mock()
            mock.return_value = db_manager
            yield db_manager
    
    @pytest.mark.asyncio
    async def test_setup_user_session(self, integration, mock_db_manager):
        """Test setup sessione utente"""
        user_id = 1
        tiktok_username = "test_user"
        session_data = {"cookies": {}, "tokens": {}}
        
        # Mock della risposta del database
        mock_session = Mock()
        mock_db_manager.create_tiktok_session.return_value = mock_session
        
        session = await integration.setup_user_session(
            user_id, tiktok_username, session_data
        )
        
        mock_db_manager.create_tiktok_session.assert_called_once_with(
            user_id, tiktok_username, session_data, "manual"
        )
        assert session == mock_session
    
    @pytest.mark.asyncio
    async def test_sync_saved_videos(self, integration, mock_db_manager):
        """Test sincronizzazione video salvati"""
        user_id = 1
        
        # Mock sessione attiva
        mock_session = Mock()
        mock_session.id = 1
        mock_session.session_data = {"cookies": {}}
        mock_db_manager.get_active_tiktok_session.return_value = mock_session
        
        # Mock scraper
        with patch.object(integration.scraper, '__aenter__'), \
             patch.object(integration.scraper, '__aexit__'), \
             patch.object(integration.scraper, 'login_with_session', return_value=True), \
             patch.object(integration.scraper, 'get_saved_videos') as mock_get_videos:
            
            # Mock video salvati
            mock_videos = [
                {
                    'video_id': '1234567890123456789',
                    'url': 'https://tiktok.com/video/1234567890123456789',
                    'title': 'Test Video',
                    'creator': 'test_creator'
                }
            ]
            mock_get_videos.return_value = mock_videos
            
            # Mock salvataggio database
            mock_saved_video = Mock()
            mock_saved_video.id = 1
            mock_saved_video.tiktok_video_id = '1234567890123456789'
            mock_saved_video.video_title = 'Test Video'
            mock_db_manager.save_tiktok_video.return_value = mock_saved_video
            
            result = await integration.sync_saved_videos(user_id)
            
            assert len(result) == 1
            assert result[0]['status'] == 'synced'
            mock_db_manager.update_tiktok_session_activity.assert_called_once()
    
    def test_get_user_library_summary(self, integration, mock_db_manager):
        """Test riepilogo libreria utente"""
        user_id = 1
        
        # Mock video con analisi
        mock_videos = [
            {
                'download_status': 'downloaded',
                'file_size_mb': 10.5,
                'analysis': {
                    'overall_score': 8.5
                },
                'saved_at': '2024-01-01T10:00:00'
            },
            {
                'download_status': 'downloaded',
                'file_size_mb': 15.2,
                'analysis': {
                    'overall_score': 7.8
                },
                'saved_at': '2024-01-02T10:00:00'
            }
        ]
        mock_db_manager.get_videos_with_analysis.return_value = mock_videos
        
        # Mock sessione attiva
        mock_session = Mock()
        mock_session.tiktok_username = "test_user"
        mock_session.is_active = True
        mock_session.last_activity = "2024-01-02T10:00:00"
        mock_db_manager.get_active_tiktok_session.return_value = mock_session
        
        summary = integration.get_user_library_summary(user_id)
        
        assert summary['total_videos'] == 2
        assert summary['downloaded_videos'] == 2
        assert summary['analyzed_videos'] == 2
        assert summary['average_score'] == 8.15
        assert summary['total_size_mb'] == 25.7
        assert summary['session']['username'] == "test_user"

class TestDatabaseIntegration:
    """Test per l'integrazione database"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock del database"""
        with patch('db.database.get_db_manager') as mock:
            db_manager = Mock()
            mock.return_value = db_manager
            yield db_manager
    
    def test_create_tiktok_session(self, mock_db):
        """Test creazione sessione TikTok"""
        user_id = 1
        username = "test_user"
        session_data = {"cookies": {}}
        
        mock_session = Mock()
        mock_db.create_tiktok_session.return_value = mock_session
        
        session = mock_db.create_tiktok_session(user_id, username, session_data)
        
        mock_db.create_tiktok_session.assert_called_once_with(
            user_id, username, session_data, "manual"
        )
        assert session == mock_session
    
    def test_save_tiktok_video(self, mock_db):
        """Test salvataggio video TikTok"""
        user_id = 1
        video_data = {
            'tiktok_video_id': '1234567890123456789',
            'video_url': 'https://tiktok.com/video/1234567890123456789',
            'video_title': 'Test Video'
        }
        
        mock_video = Mock()
        mock_db.save_tiktok_video.return_value = mock_video
        
        video = mock_db.save_tiktok_video(user_id, video_data)
        
        mock_db.save_tiktok_video.assert_called_once_with(user_id, video_data, None)
        assert video == mock_video

class TestUtilityFunctions:
    """Test per le funzioni di utilità"""
    
    @pytest.mark.asyncio
    async def test_integrate_tiktok_user(self):
        """Test integrazione utente TikTok"""
        with patch('scraper.tiktok_integration.TikTokIntegration') as mock_integration_class:
            mock_integration = Mock()
            mock_integration_class.return_value = mock_integration
            
            # Mock setup sessione
            mock_session = Mock()
            mock_integration.setup_user_session.return_value = mock_session
            
            # Mock sincronizzazione
            mock_integration.sync_saved_videos.return_value = [{'status': 'synced'}]
            
            result = await integrate_tiktok_user(
                user_id=1,
                tiktok_username="test_user",
                session_data={"cookies": {}}
            )
            
            assert result is True
            mock_integration.setup_user_session.assert_called_once()
            mock_integration.sync_saved_videos.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_sync_user_tiktok_library(self):
        """Test sincronizzazione libreria utente"""
        with patch('scraper.tiktok_integration.TikTokIntegration') as mock_integration_class:
            mock_integration = Mock()
            mock_integration_class.return_value = mock_integration
            
            # Mock sincronizzazione
            mock_integration.sync_saved_videos.return_value = [{'status': 'synced'}]
            mock_integration.download_user_videos.return_value = [{'status': 'downloaded'}]
            mock_integration.get_user_library_summary.return_value = {'total_videos': 1}
            
            result = await sync_user_tiktok_library(user_id=1)
            
            assert result['success'] is True
            assert result['synced_videos'] == 1
            assert result['downloaded_videos'] == 1
            assert 'summary' in result

# Test di integrazione end-to-end
class TestEndToEnd:
    """Test di integrazione end-to-end"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, temp_cache_dir):
        """Test workflow completo"""
        # Questo test richiede un ambiente di test completo
        # con database e browser configurati
        pass

# TEST: edge-case - Video non trovato (404)
def test_download_video_not_found(monkeypatch):
    from scraper.download_tiktok_video import download_video_for_analysis
    async def fake_download(*args, **kwargs):
        raise ValueError("Video not found")
    monkeypatch.setattr("scraper.download_tiktok_video.download_video_for_analysis", fake_download)
    with pytest.raises(ValueError, match="Video not found"):
        import asyncio
        asyncio.run(download_video_for_analysis("https://www.tiktok.com/@user/video/404"))

# TEST: edge-case - URL TikTok malformato
def test_download_video_invalid_url():
    from scraper.download_tiktok_video import TikTokVideoDownloader
    downloader = TikTokVideoDownloader(cache_dir="/tmp")
    invalid_url = "https://invalid.url"
    with pytest.raises(Exception):
        downloader.get_video_id_from_url(invalid_url)

# TEST: edge-case - Errore Playwright simulato
@pytest.mark.asyncio
def test_playwright_timeout(monkeypatch):
    from scraper.download_tiktok_video import TikTokVideoDownloader
    downloader = TikTokVideoDownloader(cache_dir="/tmp")
    async def fake_get_video_download_url(*args, **kwargs):
        raise RuntimeError("Playwright timeout")
    monkeypatch.setattr(downloader, "get_video_download_url", fake_get_video_download_url)
    with pytest.raises(RuntimeError, match="Playwright timeout"):
        import asyncio
        asyncio.run(downloader.get_video_download_url("https://www.tiktok.com/@user/video/123"))

if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v"]) 