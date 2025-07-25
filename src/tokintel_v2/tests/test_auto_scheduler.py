#!/usr/bin/env python3
# [INFO] Test per Auto-Analyze Scheduler - TokIntel v2
"""
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from scheduler.auto_scheduler import (
    AutoAnalyzeScheduler,
    start_auto_analyzer,
    stop_auto_analyzer,
    get_auto_analyzer_status,
    get_scheduler
)

class TestAutoAnalyzeScheduler:
    """Test per la classe AutoAnalyzeScheduler"""
    
    def test_scheduler_creation(self):
        """Test che lo scheduler venga creato correttamente"""
        scheduler = AutoAnalyzeScheduler()
        
        assert scheduler is not None
        assert scheduler.is_running == False
        assert scheduler.current_user_id is None
        assert scheduler.current_interval is None
        assert scheduler.scheduler is not None
    
    @patch('scheduler.auto_scheduler.AsyncIOScheduler')
    def test_start_auto_analyzer_success(self, mock_scheduler_class):
        """Test avvio riuscito dello scheduler"""
        # Mock dello scheduler
        mock_scheduler = Mock()
        mock_scheduler_class.return_value = mock_scheduler
        
        scheduler = AutoAnalyzeScheduler()
        scheduler.scheduler = mock_scheduler
        
        # Test avvio
        result = scheduler.start_auto_analyzer(user_id=999, interval_minutes=1)
        
        assert result == True
        assert scheduler.is_running == True
        assert scheduler.current_user_id == 999
        assert scheduler.current_interval == 1
        
        # Verifica che i metodi dello scheduler siano stati chiamati
        mock_scheduler.add_job.assert_called_once()
        mock_scheduler.add_listener.assert_called_once()
        mock_scheduler.start.assert_called_once()
    
    @patch('scheduler.auto_scheduler.AsyncIOScheduler')
    def test_start_auto_analyzer_failure(self, mock_scheduler_class):
        """Test avvio fallito dello scheduler"""
        # Mock dello scheduler che solleva un'eccezione
        mock_scheduler = Mock()
        mock_scheduler.add_job.side_effect = Exception("Test error")
        mock_scheduler_class.return_value = mock_scheduler
        
        scheduler = AutoAnalyzeScheduler()
        scheduler.scheduler = mock_scheduler
        
        # Test avvio con errore
        result = scheduler.start_auto_analyzer(user_id=999, interval_minutes=1)
        
        assert result == False
        assert scheduler.is_running == False
    
    @patch('scheduler.auto_scheduler.AsyncIOScheduler')
    def test_stop_scheduler(self, mock_scheduler_class):
        """Test fermata dello scheduler"""
        mock_scheduler = Mock()
        mock_scheduler_class.return_value = mock_scheduler
        
        scheduler = AutoAnalyzeScheduler()
        scheduler.scheduler = mock_scheduler
        scheduler.is_running = True
        
        # Test fermata
        scheduler.stop_scheduler()
        
        assert scheduler.is_running == False
        mock_scheduler.shutdown.assert_called_once_with(wait=False)
    
    def test_get_status(self):
        """Test recupero status dello scheduler"""
        scheduler = AutoAnalyzeScheduler()
        scheduler.is_running = True
        scheduler.current_user_id = 123
        scheduler.current_interval = 30
        
        # Mock del metodo get_jobs
        scheduler.scheduler.get_jobs = Mock(return_value=[Mock(), Mock()])
        
        status = scheduler.get_status()
        
        assert status['is_running'] == True
        assert status['user_id'] == 123
        assert status['interval_minutes'] == 30
        assert status['jobs'] == 2

class TestSchedulerFunctions:
    """Test per le funzioni di utilità dello scheduler"""
    
    def test_get_scheduler_singleton(self):
        """Test che get_scheduler restituisca sempre la stessa istanza"""
        # Reset dell'istanza globale
        import scheduler.auto_scheduler
        scheduler.auto_scheduler._scheduler_instance = None
        
        scheduler1 = get_scheduler()
        scheduler2 = get_scheduler()
        
        assert scheduler1 is scheduler2
    
    @patch('scheduler.auto_scheduler.get_scheduler')
    def test_start_auto_analyzer_function(self, mock_get_scheduler):
        """Test della funzione start_auto_analyzer"""
        mock_scheduler = Mock()
        mock_scheduler.start_auto_analyzer.return_value = True
        mock_get_scheduler.return_value = mock_scheduler
        
        result = start_auto_analyzer(user_id=999, interval_minutes=1)
        
        assert result == True
        mock_scheduler.start_auto_analyzer.assert_called_once_with(999, 1)
    
    @patch('scheduler.auto_scheduler.get_scheduler')
    def test_stop_auto_analyzer_function(self, mock_get_scheduler):
        """Test della funzione stop_auto_analyzer"""
        mock_scheduler = Mock()
        mock_get_scheduler.return_value = mock_scheduler
        
        stop_auto_analyzer()
        
        mock_scheduler.stop_scheduler.assert_called_once()
    
    @patch('scheduler.auto_scheduler.get_scheduler')
    def test_get_auto_analyzer_status_function(self, mock_get_scheduler):
        """Test della funzione get_auto_analyzer_status"""
        mock_scheduler = Mock()
        mock_scheduler.get_status.return_value = {'test': 'status'}
        mock_get_scheduler.return_value = mock_scheduler
        
        status = get_auto_analyzer_status()
        
        assert status == {'test': 'status'}
        mock_scheduler.get_status.assert_called_once()

class TestSchedulerIntegration:
    """Test di integrazione per lo scheduler"""
    
    @pytest.mark.asyncio
    async def test_analysis_job_execution(self):
        """Test esecuzione del job di analisi"""
        scheduler = AutoAnalyzeScheduler()
        
        # Mock della funzione di analisi
        with patch('scheduler.auto_scheduler.analyze_user_pending_videos') as mock_analyze:
            mock_analyze.return_value = {
                'analyzed': 3,
                'errors': 1,
                'total_videos': 4
            }
            
            # Esegui il job di analisi
            await scheduler._run_analysis_job(user_id=999)
            
            # Verifica che la funzione di analisi sia stata chiamata
            mock_analyze.assert_called_once_with(999)
    
    @pytest.mark.asyncio
    async def test_analysis_job_error_handling(self):
        """Test gestione errori nel job di analisi"""
        scheduler = AutoAnalyzeScheduler()
        
        # Mock della funzione di analisi che solleva un'eccezione
        with patch('scheduler.auto_scheduler.analyze_user_pending_videos') as mock_analyze:
            mock_analyze.side_effect = Exception("Test analysis error")
            
            # Esegui il job di analisi (non deve sollevare eccezioni)
            await scheduler._run_analysis_job(user_id=999)
            
            # Verifica che la funzione di analisi sia stata chiamata
            mock_analyze.assert_called_once_with(999)

if __name__ == "__main__":
    pytest.main([__file__]) 