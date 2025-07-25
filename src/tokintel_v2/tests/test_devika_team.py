#!/usr/bin/env python3
"""
Test unitari per DevikaAgentTeam
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Aggiungi il path del progetto
sys.path.append(str(Path(__file__).parent.parent))

from agent.devika_team import DevikaAgentTeam, run_devika_team_analysis, AgentAnalysis, TeamAnalysisResult

class TestDevikaAgentTeam:
    """Test suite per DevikaAgentTeam"""
    
    @pytest.fixture
    def config(self):
        """Configurazione di test"""
        return {
            'llm': {
                'model': 'test-model',
                'temperature': 0.7
            }
        }
    
    @pytest.fixture
    def team(self, config):
        """Istanza del team per i test"""
        return DevikaAgentTeam(config)
    
    @pytest.fixture
    def sample_content(self):
        """Contenuto di esempio per i test"""
        return """
        Scopri i 3 segreti per il successo nel business! 
        Se stai lottando per far crescere la tua azienda, 
        questo video ti mostrerà esattamente cosa fare.
        #business #successo #motivazione
        """
    
    def test_team_initialization(self, config):
        """Test inizializzazione del team"""
        team = DevikaAgentTeam(config)
        assert team is not None
        assert hasattr(team, 'agents')
        assert len(team.agents) == 3
        assert 'strategist' in team.agents
        assert 'copywriter' in team.agents
        assert 'analyst' in team.agents
    
    def test_agent_creation(self, team):
        """Test creazione degli agenti"""
        # Test Strategist
        strategist = team.agents['strategist']
        assert strategist['name'] == 'Strategist'
        assert 'content_strategy' in strategist['expertise']
        
        # Test Copywriter
        copywriter = team.agents['copywriter']
        assert copywriter['name'] == 'Copywriter'
        assert 'viral_hooks' in copywriter['expertise']
        
        # Test Analyst
        analyst = team.agents['analyst']
        assert analyst['name'] == 'Analyst'
        assert 'kpi_analysis' in analyst['expertise']
    
    @pytest.mark.asyncio
    async def test_team_analysis(self, team, sample_content):
        """Test analisi completa del team"""
        metadata = {'title': 'Video di Test'}
        result = await team.run_team_analysis(sample_content, metadata)
        
        assert isinstance(result, TeamAnalysisResult)
        assert result.video_title == 'Video di Test'
        assert 0 <= result.overall_score <= 1
        assert 0 <= result.viral_potential <= 1
        assert 0 <= result.engagement_prediction <= 1
        assert len(result.agent_analyses) == 3
        assert len(result.team_recommendations) > 0
        assert len(result.priority_actions) > 0
    
    @pytest.mark.asyncio
    async def test_individual_agent_analysis(self, team, sample_content):
        """Test analisi dei singoli agenti"""
        metadata = {}
        
        # Test Strategist
        strategist_result = await team._run_agent_analysis('strategist', sample_content, metadata)
        assert isinstance(strategist_result, AgentAnalysis)
        assert strategist_result.agent_name == 'Strategist'
        assert strategist_result.confidence > 0
        
        # Test Copywriter
        copywriter_result = await team._run_agent_analysis('copywriter', sample_content, metadata)
        assert isinstance(copywriter_result, AgentAnalysis)
        assert copywriter_result.agent_name == 'Copywriter'
        assert copywriter_result.confidence > 0
        
        # Test Analyst
        analyst_result = await team._run_agent_analysis('analyst', sample_content, metadata)
        assert isinstance(analyst_result, AgentAnalysis)
        assert analyst_result.agent_name == 'Analyst'
        assert analyst_result.confidence > 0
    
    def test_tone_analysis(self, team, sample_content):
        """Test analisi del tone of voice"""
        tone = team._analyze_tone(sample_content)
        assert isinstance(tone, str)
        assert tone in ["Emozionale e coinvolgente", "Formale e professionale", "Bilanciato"]
    
    def test_audience_identification(self, team, sample_content):
        """Test identificazione audience"""
        audience = team._identify_audience(sample_content)
        assert isinstance(audience, str)
        assert "business" in sample_content.lower()
        assert "Imprenditori" in audience or "Audience generale" in audience
    
    def test_viral_potential_calculation(self, team, sample_content):
        """Test calcolo potenziale virale"""
        agent_results = []
        viral_potential = team._calculate_viral_potential(sample_content, agent_results)
        assert 0 <= viral_potential <= 1
    
    def test_engagement_prediction(self, team):
        """Test predizione engagement"""
        # Crea agenti di test
        test_agents = [
            AgentAnalysis(
                agent_name="Test Agent 1",
                analysis_type="Test",
                insights={},
                confidence=0.8,
                recommendations=[],
                timestamp=None
            ),
            AgentAnalysis(
                agent_name="Test Agent 2",
                analysis_type="Test",
                insights={},
                confidence=0.6,
                recommendations=[],
                timestamp=None
            )
        ]
        
        prediction = team._calculate_engagement_prediction(test_agents)
        assert prediction == 0.7  # Media di 0.8 e 0.6
    
    def test_priority_actions_identification(self, team):
        """Test identificazione azioni prioritarie"""
        recommendations = [
            "Azione importante da fare subito",
            "Migliora la qualità",
            "Urgente: ottimizza il titolo",
            "Aggiungi più contenuti"
        ]
        
        priority_actions = team._identify_priority_actions(recommendations)
        assert len(priority_actions) <= 3
        assert any("importante" in action.lower() for action in priority_actions)
        assert any("urgente" in action.lower() for action in priority_actions)
    
    @pytest.mark.asyncio
    async def test_utility_function(self, sample_content):
        """Test funzione di utilità run_devika_team_analysis"""
        result = await run_devika_team_analysis(sample_content)
        
        assert isinstance(result, dict)
        assert 'video_title' in result
        assert 'overall_score' in result
        assert 'viral_potential' in result
        assert 'engagement_prediction' in result
        assert 'agent_analyses' in result
        assert 'team_recommendations' in result
        assert 'priority_actions' in result
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_error_handling(self, team):
        """Test gestione errori"""
        # Test con contenuto vuoto
        result = await team.run_team_analysis("", {})
        assert isinstance(result, TeamAnalysisResult)
        assert result.overall_score >= 0
    
    def test_fallback_analysis(self, team):
        """Test analisi di fallback"""
        fallback = team._create_fallback_analysis('test_agent', 'test content')
        assert isinstance(fallback, AgentAnalysis)
        assert 'Fallback' in fallback.agent_name
        assert fallback.confidence == 0.3

class TestIntegration:
    """Test di integrazione"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test workflow completo"""
        config = {'llm': {'model': 'test'}}
        content = "Video motivazionale per imprenditori #business #successo"
        metadata = {'title': 'Test Video'}
        
        # Esegui analisi completa
        result = await run_devika_team_analysis(content, config)
        
        # Verifica struttura risultato
        assert result['video_title'] in ['Test Video', 'Video TikTok']  # Gestisce entrambi i casi
        assert result['overall_score'] > 0
        assert len(result['agent_analyses']) == 3
        
        # Verifica che ogni agente abbia prodotto risultati
        agent_names = [analysis['agent_name'] for analysis in result['agent_analyses']]
        assert 'Strategist' in agent_names
        assert 'Copywriter' in agent_names
        assert 'Analyst' in agent_names

if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v"]) 