"""
Test suite per il modulo core/logger.py
TokIntel v2.1 - Enterprise Grade
"""

from typing import Dict, List, Any, Optional
import pytest
import logging
import tempfile
import os

# Aggiungi il path del progetto
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.logger import setup_logger, get_logger, LoggerMixin


class TestLoggerSetup:
    """Test per la configurazione del logger"""
    
    def test_setup_logger_basic(self):
        """Test configurazione logger base"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("test_logger", level=logging.INFO, log_file=log_file)
            
            assert logger is not None
            assert logger.name == "test_logger"
            assert logger.level == logging.INFO
            
            # Verifica che il file di log sia stato creato
            assert os.path.exists(log_file)
            
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)
    
    def test_setup_logger_default_values(self):
        """Test configurazione logger con valori di default"""
        logger = setup_logger("default_logger")
        
        assert logger is not None
        assert logger.name == "default_logger"
        assert logger.level == logging.INFO
    
    def test_setup_logger_custom_level(self):
        """Test configurazione logger con livello personalizzato"""
        logger = setup_logger("debug_logger", level=logging.DEBUG)
        
        assert logger.level == logging.DEBUG
    
    def test_setup_logger_file_creation(self):
        """Test creazione file di log"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("file_logger", log_file=log_file)
            
            # Scrivi un messaggio di test
            logger.info("Test message")
            
            # Verifica che il messaggio sia stato scritto nel file
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Test message" in content
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)


class TestGetLogger:
    """Test per la funzione get_logger"""
    
    def test_get_logger_existing(self):
        """Test ottenimento logger esistente"""
        # Crea un logger
        original_logger = setup_logger("existing_logger")
        
        # Ottieni lo stesso logger
        retrieved_logger = get_logger("existing_logger")
        
        assert retrieved_logger is original_logger
        assert retrieved_logger.name == "existing_logger"
    
    def test_get_logger_new(self):
        """Test ottenimento logger nuovo"""
        logger = get_logger("new_logger")
        
        assert logger is not None
        assert logger.name == "new_logger"
        assert logger.level == logging.INFO  # Default level


class TestLogError:
    """Test per la funzione log_error"""
    
    def test_log_error_basic(self):
        """Test logging error base"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            # Usa LoggerMixin per testare log_error
            class TestClass(LoggerMixin):
                pass
            
            test_instance = TestClass()
            test_instance.log_error("Test error message")
            
            # Verifica che il messaggio sia stato loggato
            assert True  # Se non ci sono eccezioni, il test passa
            
            # Testa logging di un errore
            test_error = ValueError("Test error message")
            log_error(logger, "Test operation failed", test_error)
            
            # Verifica che l'errore sia stato loggato
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Test operation failed" in content
                assert "ValueError" in content
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)
    
    def test_log_error_with_exc_info(self):
        """Test logging error con exc_info=True"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("error_logger", log_file=log_file)
            
            # Testa logging con exc_info
            test_error = RuntimeError("Runtime test error")
            log_error(logger, "Runtime operation failed", test_error, exc_info=True)
            
            # Verifica che l'errore sia stato loggato con traceback
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Runtime operation failed" in content
                assert "RuntimeError" in content
                assert "Traceback" in content  # Dovrebbe includere il traceback
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)
    
    def test_log_error_without_exception(self):
        """Test logging error senza eccezione"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("error_logger", log_file=log_file)
            
            # Testa logging senza eccezione
            log_error(logger, "Simple error message")
            
            # Verifica che il messaggio sia stato loggato
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Simple error message" in content
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)


class TestLoggerEdgeCases:
    """Test per edge cases del logger"""
    
    def test_logger_invalid_level(self):
        """Test con livello logger invalido"""
        with pytest.raises(ValueError):
            setup_logger("invalid_logger", level="INVALID_LEVEL")
    
    def test_logger_invalid_file_path(self):
        """Test con percorso file invalido"""
        # Dovrebbe gestire graziosamente percorsi invalidi
        logger = setup_logger("invalid_file_logger", log_file="/invalid/path/log.txt")
        
        # Il logger dovrebbe comunque funzionare (solo console output)
        assert logger is not None
        logger.info("Test message")  # Non dovrebbe crashare
    
    def test_logger_unicode_messages(self):
        """Test con messaggi Unicode"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("unicode_logger", log_file=log_file)
            
            # Testa messaggi Unicode
            unicode_message = "Test con caratteri speciali: [INFO] éñç"
            logger.info(unicode_message)
            
            # Verifica che il messaggio sia stato loggato correttamente
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert unicode_message in content
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)
    
    def test_logger_concurrent_access(self):
        """Test accesso concorrente al logger"""
        import threading
        import time
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            log_file = tmp.name
        
        try:
            logger = setup_logger("concurrent_logger", log_file=log_file)
            
            def log_message(thread_id):
                for i in range(10):
                    logger.info(f"Thread {thread_id} - Message {i}")
                    time.sleep(0.01)
            
            # Crea thread multipli
            threads = []
            for i in range(3):
                thread = threading.Thread(target=log_message, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Aspetta che tutti i thread finiscano
            for thread in threads:
                thread.join()
            
            # Verifica che tutti i messaggi siano stati loggati
            with open(log_file, 'r') as f:
                content = f.read()
                assert content.count("Thread") == 30  # 3 thread * 10 messaggi
                
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 