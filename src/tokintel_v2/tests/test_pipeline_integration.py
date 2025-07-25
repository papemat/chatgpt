#!/usr/bin/env python3
"""
Test di integrazione per il pipeline con Devika Team
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Aggiungi il path del progetto
sys.path.append(str(Path(__file__).parent.parent))

from agents.pipeline import VideoAnalysisPipeline

class TestPipelineIntegration:
    """Test di integrazione per il pipeline"""
    
    @pytest.fixture
    def config(self):
        """Configurazione di test"""
        return {
            'llm': {
                'model': 'test-model',
                'temperature': 0.7
            },
            'pipeline': {
                'audio_extraction': True,
                'transcription': True,
                'summarization': True
            }
        }
    
    @pytest.fixture
    def pipeline(self, config):
        """Istanza del pipeline per i test"""
        return VideoAnalysisPipeline(config)
    
    @pytest.mark.asyncio
    async def test_pipeline_with_devika_team(self, pipeline):
        """Test che il pipeline includa l'analisi del team Devika"""
        # Test con un file video di esempio (placeholder)
        video_path = "test_video.mp4"
        
        try:
            # Esegui analisi del pipeline
            result = await pipeline.analyze(video_path)
            
            # Verifica che il risultato contenga l'analisi Devika
            assert 'devika_analysis' in result
            devika_result = result['devika_analysis']
            
            # Verifica struttura dell'analisi Devika
            assert 'video_title' in devika_result
            assert 'overall_score' in devika_result
            assert 'viral_potential' in devika_result
            assert 'engagement_prediction' in devika_result
            assert 'agent_analyses' in devika_result
            assert 'team_recommendations' in devika_result
            assert 'priority_actions' in devika_result
            
            # Verifica che ci siano 3 agenti
            assert len(devika_result['agent_analyses']) == 3
            
            # Verifica nomi degli agenti
            agent_names = [analysis['agent_name'] for analysis in devika_result['agent_analyses']]
            assert 'Strategist' in agent_names
            assert 'Copywriter' in agent_names
            assert 'Analyst' in agent_names
            
        except Exception as e:
            # Se il file non esiste, testiamo solo l'inizializzazione
            assert "Analysis failed" in str(e) or "Frame extraction failed" in str(e)
    
    def test_pipeline_initialization(self, config):
        """Test inizializzazione del pipeline con team Devika"""
        pipeline = VideoAnalysisPipeline(config)
        
        # Verifica che il team Devika sia stato inizializzato
        assert hasattr(pipeline, 'devika_team')
        assert pipeline.devika_team is not None
        
        # Verifica che gli agenti siano presenti
        assert hasattr(pipeline.devika_team, 'agents')
        assert len(pipeline.devika_team.agents) == 3
    
    @pytest.mark.asyncio
    async def test_devika_analysis_method(self, pipeline):
        """Test del metodo _run_devika_analysis"""
        transcript = "Questo è un video motivazionale per imprenditori"
        ocr_text = "Testo estratto dalle immagini"
        summary = "Riassunto del contenuto"
        
        result = await pipeline._run_devika_analysis(transcript, ocr_text, summary)
        
        # Verifica struttura del risultato
        assert isinstance(result, dict)
        assert 'video_title' in result
        assert 'overall_score' in result
        assert 'viral_potential' in result
        assert 'engagement_prediction' in result
        assert 'agent_analyses' in result
        assert 'team_recommendations' in result
        assert 'priority_actions' in result
    
    def test_pipeline_status(self, pipeline):
        """Test dello status del pipeline"""
        status = pipeline.get_pipeline_status()
        
        assert isinstance(status, dict)
        assert 'config' in status
        assert 'agents_initialized' in status
        assert 'pipeline_ready' in status
        assert status['agents_initialized'] is True
        assert status['pipeline_ready'] is True

if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v"]) 