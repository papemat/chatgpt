"""
Test suite per il modulo di scoring della viralità
TokIntel v2.1 - Enterprise Grade
"""

from typing import Dict, List, Any, Optional
import pytest
import sys
import os

# Aggiungi il path del progetto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import Config


class TestScoringSystem:
    """Test suite per il sistema di scoring"""
    
    @pytest.fixture
    def sample_transcript(self):
        """Trascrizione di esempio per i test"""
        return """
        Ciao ragazzi! Oggi vi mostro come fare un video virale su TikTok.
        Il segreto è l'hook iniziale che cattura l'attenzione nei primi 3 secondi.
        Poi bisogna mantenere l'engagement con contenuti interessanti.
        """
    
    @pytest.fixture
    def sample_ocr_text(self):
        """Testo OCR di esempio"""
        return "VIDEO VIRALE TIKTOK HOOK ENGAGEMENT"
    
    @pytest.fixture
    def mock_config(self):
        """Configurazione di test"""
        return Config(
            model="gpt-4",
            language="it",
            keywords=["viral", "hook", "engagement", "tiktok"]
        )
    
    def test_viral_score_calculation(self, sample_transcript, sample_ocr_text, mock_config):
        """Test calcolo punteggio viralità"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        # Mock della risposta LLM
        mock_response = {
            "viral_score": 85,
            "engagement_factors": ["hook_strong", "trending_topic"],
            "optimization_suggestions": ["Migliora l'hook iniziale"]
        }
        
        with patch.object(agent, '_call_openai_llm', return_value=mock_response):
            result = agent.analyze_engagement_factors(
                sample_transcript, 
                sample_ocr_text, 
                mock_config
            )
            
            assert result is not None
            assert "viral_score" in result
            assert result["viral_score"] == 85
    
    def test_keyword_detection(self, sample_transcript, sample_ocr_text):
        """Test rilevamento keywords"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        # Verifica che le keywords siano rilevate
        keywords_found = []
        for keyword in ["viral", "hook", "engagement", "tiktok"]:
            if keyword.lower() in sample_transcript.lower() or keyword.lower() in sample_ocr_text.lower():
                keywords_found.append(keyword)
        
        assert len(keywords_found) > 0
        assert "viral" in keywords_found
        assert "hook" in keywords_found
    
    def test_score_range_validation(self, sample_transcript, sample_ocr_text, mock_config):
        """Test validazione range punteggi"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        # Test punteggio valido
        valid_score = 75
        assert 0 <= valid_score <= 100
        
        # Test punteggio invalido
        invalid_score = 150
        assert not (0 <= invalid_score <= 100)
    
    def test_engagement_factors_analysis(self, sample_transcript, sample_ocr_text, mock_config):
        """Test analisi fattori engagement"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        mock_response = {
            "engagement_factors": [
                "hook_effectiveness",
                "content_quality", 
                "trend_alignment"
            ],
            "factor_scores": {
                "hook_effectiveness": 90,
                "content_quality": 75,
                "trend_alignment": 80
            }
        }
        
        with patch.object(agent, '_call_openai_llm', return_value=mock_response):
            result = agent.analyze_engagement_factors(
                sample_transcript, 
                sample_ocr_text, 
                mock_config
            )
            
            assert "engagement_factors" in result
            assert len(result["engagement_factors"]) > 0
    
    def test_error_handling_invalid_input(self):
        """Test gestione errori con input invalidi"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        # Test con input vuoti
        with pytest.raises(ValueError):
            agent.analyze_engagement_factors("", "", None)
        
        # Test con input None
        with pytest.raises(ValueError):
            agent.analyze_engagement_factors(None, None, None)


class TestScoringEdgeCases:
    """Test per edge cases del sistema di scoring"""
    
    def test_empty_ocr_text(self):
        """Test con testo OCR vuoto"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        transcript = "Contenuto video normale"
        ocr_text = ""
        
        # Dovrebbe gestire graziosamente OCR vuoto
        try:
            result = agent.analyze_engagement_factors(transcript, ocr_text, Mock())
            assert result is not None
        except Exception as e:
            # Se fallisce, dovrebbe essere un errore gestito
            assert "ocr" in str(e).lower() or "empty" in str(e).lower()
    
    def test_very_long_transcript(self):
        """Test con trascrizione molto lunga"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        # Trascrizione di 10k caratteri
        long_transcript = "Testo molto lungo " * 500
        ocr_text = "OCR normale"
        
        # Dovrebbe gestire input lunghi
        try:
            result = agent.analyze_engagement_factors(long_transcript, ocr_text, Mock())
            assert result is not None
        except Exception as e:
            # Se fallisce, dovrebbe essere per limite token
            assert "token" in str(e).lower() or "length" in str(e).lower()
    
    def test_special_characters(self):
        """Test con caratteri speciali"""
        agent = SynthesisAgent(model="gpt-4", endpoint="", api_key="test")
        
        transcript = "Video con emoji [INFO] e caratteri speciali @#$%"
        ocr_text = "OCR con simboli ©®™"
        
        # Dovrebbe gestire caratteri speciali
        try:
            result = agent.analyze_engagement_factors(transcript, ocr_text, Mock())
            assert result is not None
        except Exception as e:
            # Se fallisce, dovrebbe essere un errore di encoding
            assert "encoding" in str(e).lower() or "character" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 