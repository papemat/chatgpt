"""
Unit tests for prompts module
"""

from typing import Dict, List, Any, Optional
import pytest


class TestPromptTemplates:
    """Test PromptTemplates functionality"""
    
    def test_build_summary_prompt(self):
        """Test summary prompt building"""
        transcript = "Questo è un video motivazionale"
        ocr_text = "Testo visivo importante"
        
        prompt = PromptTemplates.build_summary_prompt(transcript, ocr_text)
        
        assert "Questo è un video motivazionale" in prompt
        assert "Testo visivo importante" in prompt
        assert "Analizza il seguente contenuto video TikTok" in prompt
        assert "Tema principale" in prompt
        assert "Emozioni" in prompt
        assert "Hook" in prompt
    
    def test_build_engagement_analysis_prompt(self):
        """Test engagement analysis prompt building"""
        transcript = "Contenuto di engagement"
        ocr_text = "Call to action"
        
        prompt = PromptTemplates.build_engagement_analysis_prompt(transcript, ocr_text)
        
        assert "Contenuto di engagement" in prompt
        assert "Call to action" in prompt
        assert "fattori di engagement" in prompt
        assert "scala da 1 a 10" in prompt
        assert "JSON" in prompt
    
    def test_build_viral_potential_prompt(self):
        """Test viral potential prompt building"""
        transcript = "Contenuto virale"
        ocr_text = "Testo virale"
        keywords = ["viral", "trend", "hot"]
        
        prompt = PromptTemplates.build_viral_potential_prompt(transcript, ocr_text, keywords)
        
        assert "Contenuto virale" in prompt
        assert "Testo virale" in prompt
        assert "viral, trend, hot" in prompt
        assert "potenziale virale" in prompt
        assert "Probabilità di diventare virale" in prompt
    
    def test_build_content_optimization_prompt(self):
        """Test content optimization prompt building"""
        transcript = "Contenuto da ottimizzare"
        ocr_text = "Testo da migliorare"
        target_score = 8.5
        
        prompt = PromptTemplates.build_content_optimization_prompt(transcript, ocr_text, target_score)
        
        assert "Contenuto da ottimizzare" in prompt
        assert "Testo da migliorare" in prompt
        assert "8.5" in prompt
        assert "ottimizzazioni" in prompt
        assert "Hook più efficace" in prompt
    
    def test_build_audience_analysis_prompt(self):
        """Test audience analysis prompt building"""
        transcript = "Contenuto per audience"
        ocr_text = "Target specifico"
        
        prompt = PromptTemplates.build_audience_analysis_prompt(transcript, ocr_text)
        
        assert "Contenuto per audience" in prompt
        assert "Target specifico" in prompt
        assert "target audience" in prompt
        assert "Età target" in prompt
        assert "Interessi principali" in prompt
    
    def test_build_trend_analysis_prompt(self):
        """Test trend analysis prompt building"""
        transcript = "Contenuto trendy"
        ocr_text = "Testo in trend"
        current_trends = ["trend1", "trend2", "trend3"]
        
        prompt = PromptTemplates.build_trend_analysis_prompt(transcript, ocr_text, current_trends)
        
        assert "Contenuto trendy" in prompt
        assert "Testo in trend" in prompt
        assert "trend1, trend2, trend3" in prompt
        assert "tendenze attuali" in prompt
        assert "Allineamento con le tendenze" in prompt


class TestPromptManager:
    """Test PromptManager functionality"""
    
    def test_init(self):
        """Test PromptManager initialization"""
        manager = PromptManager()
        assert manager.templates is not None
        assert manager.prompt_history == []
    
    def test_get_summary_prompt(self):
        """Test getting summary prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("summary", transcript="test", ocr_text="test")
        
        assert "test" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "summary"
    
    def test_get_engagement_prompt(self):
        """Test getting engagement prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("engagement", transcript="test", ocr_text="test")
        
        assert "test" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "engagement"
    
    def test_get_viral_prompt(self):
        """Test getting viral prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("viral", transcript="test", ocr_text="test", keywords=["test"])
        
        assert "test" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "viral"
    
    def test_get_optimization_prompt(self):
        """Test getting optimization prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("optimization", transcript="test", ocr_text="test", target_score=8.0)
        
        assert "test" in prompt
        assert "8.0" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "optimization"
    
    def test_get_audience_prompt(self):
        """Test getting audience prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("audience", transcript="test", ocr_text="test")
        
        assert "test" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "audience"
    
    def test_get_trend_prompt(self):
        """Test getting trend prompt"""
        manager = PromptManager()
        
        prompt = manager.get_prompt("trend", transcript="test", ocr_text="test", current_trends=["trend1"])
        
        assert "test" in prompt
        assert "trend1" in prompt
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["type"] == "trend"
    
    def test_invalid_prompt_type(self):
        """Test invalid prompt type handling"""
        manager = PromptManager()
        
        with pytest.raises(ValueError, match="Unknown prompt type"):
            manager.get_prompt("invalid_type")
    
    def test_prompt_history_tracking(self):
        """Test prompt history tracking"""
        manager = PromptManager()
        
        # Generate multiple prompts
        manager.get_prompt("summary", transcript="test1", ocr_text="test1")
        manager.get_prompt("engagement", transcript="test2", ocr_text="test2")
        manager.get_prompt("viral", transcript="test3", ocr_text="test3", keywords=["test"])
        
        assert len(manager.prompt_history) == 3
        assert manager.prompt_history[0]["type"] == "summary"
        assert manager.prompt_history[1]["type"] == "engagement"
        assert manager.prompt_history[2]["type"] == "viral"
    
    def test_get_prompt_stats(self):
        """Test getting prompt statistics"""
        manager = PromptManager()
        
        # Generate prompts
        manager.get_prompt("summary", transcript="test", ocr_text="test")
        manager.get_prompt("summary", transcript="test", ocr_text="test")
        manager.get_prompt("engagement", transcript="test", ocr_text="test")
        
        stats = manager.get_prompt_stats()
        
        assert stats["total_prompts"] == 3
        assert stats["by_type"]["summary"] == 2
        assert stats["by_type"]["engagement"] == 1
    
    def test_prompt_kwargs_tracking(self):
        """Test that prompt kwargs are tracked correctly"""
        manager = PromptManager()
        
        kwargs = {"transcript": "test", "ocr_text": "test", "keywords": ["test"]}
        manager.get_prompt("viral", **kwargs)
        
        assert len(manager.prompt_history) == 1
        assert manager.prompt_history[0]["kwargs"] == kwargs 