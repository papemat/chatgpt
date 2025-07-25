"""
[INFO] Test Suite per Funzionalità Pro - TokIntel v2.1
Test completi per chat agents, PDF exporter e database
"""

import pytest
import tempfile
import os
import json
from datetime import datetime
from unittest.mock import Mock, patch

# Import delle funzionalità da testare
try:
    from ui.chat_agents import AgentChat
    from utils.pdf_exporter import PDFExporter, export_analysis_to_pdf, create_sample_report
    from db.database import DatabaseManager, init_database, save_analysis_result, get_analysis_history
    PRO_FEATURES_AVAILABLE = True
except ImportError:
    PRO_FEATURES_AVAILABLE = False

@pytest.mark.skipif(not PRO_FEATURES_AVAILABLE, reason="Funzionalità Pro non disponibili")
class TestChatAgents:
    """Test per il sistema di chat con agenti AI"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.chat = AgentChat()
    
    def test_agent_initialization(self):
        """Test inizializzazione agenti"""
        assert len(self.chat.agents) == 3
        assert "strategist" in self.chat.agents
        assert "copywriter" in self.chat.agents
        assert "analyst" in self.chat.agents
    
    def test_agent_properties(self):
        """Test proprietà degli agenti"""
        strategist = self.chat.agents["strategist"]
        assert "name" in strategist
        assert "role" in strategist
        assert "avatar" in strategist
        assert "expertise" in strategist
        assert len(strategist["expertise"]) > 0
    
    def test_strategist_response(self):
        """Test risposta dello strategist"""
        response = self.chat.get_agent_response("strategist", "Come migliorare il mio video?")
        assert isinstance(response, str)
        assert len(response) > 10
        assert "[TARGET]" in response or "strategico" in response.lower()
    
    def test_copywriter_response(self):
        """Test risposta del copywriter"""
        response = self.chat.get_agent_response("copywriter", "Scrivere un hook efficace")
        assert isinstance(response, str)
        assert len(response) > 10
        assert "✍️" in response or "hook" in response.lower()
    
    def test_analyst_response(self):
        """Test risposta dell'analyst"""
        response = self.chat.get_agent_response("analyst", "Analisi delle metriche")
        assert isinstance(response, str)
        assert len(response) > 10
        assert "[REPORT]" in response or "dati" in response.lower()
    
    def test_invalid_agent(self):
        """Test agente non valido"""
        response = self.chat.get_agent_response("invalid_agent", "test")
        assert "non ho capito" in response.lower()

@pytest.mark.skipif(not PRO_FEATURES_AVAILABLE, reason="Funzionalità Pro non disponibili")
class TestPDFExporter:
    """Test per l'esportazione PDF"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_data = {
            "video_title": "Test Video TikTok",
            "analysis_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "overall_score": 85.5,
            "summary": "Video di test per verificare l'esportazione PDF",
            "key_points": [
                "Hook efficace",
                "Contenuto di valore",
                "Call-to-action chiara"
            ],
            "metrics": {
                "engagement_rate": 4.2,
                "completion_rate": 75,
                "share_rate": 2.1,
                "comment_rate": 1.8,
                "like_rate": 3.5
            },
            "keywords": ["test", "tiktok", "pdf", "analisi"],
            "suggested_hashtags": ["#test", "#tiktok", "#analisi"],
            "recommendations": [
                {
                    "title": "Migliora l'Hook",
                    "description": "Inizia con una domanda più provocatoria"
                }
            ],
            "duration": "30 secondi",
            "resolution": "1080x1920",
            "format": "MP4",
            "ai_model": "GPT-4",
            "version": "v2.1"
        }
    
    def teardown_method(self):
        """Cleanup dopo ogni test"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_pdf_exporter_initialization(self):
        """Test inizializzazione PDF exporter"""
        exporter = PDFExporter()
        assert exporter is not None
        assert hasattr(exporter, 'pdf')
    
    def test_create_sample_report(self):
        """Test creazione report di esempio"""
        output_file = create_sample_report()
        assert os.path.exists(output_file)
        assert output_file.endswith('.pdf')
        assert os.path.getsize(output_file) > 1000  # Almeno 1KB
    
    def test_export_analysis_to_pdf(self):
        """Test esportazione analisi in PDF"""
        output_path = os.path.join(self.temp_dir, "test_report.pdf")
        result_path = export_analysis_to_pdf(self.sample_data, output_path)
        
        assert result_path == output_path
        assert os.path.exists(result_path)
        assert result_path.endswith('.pdf')
        assert os.path.getsize(result_path) > 1000
    
    def test_pdf_content_structure(self):
        """Test struttura contenuto PDF"""
        output_path = os.path.join(self.temp_dir, "structure_test.pdf")
        export_analysis_to_pdf(self.sample_data, output_path)
        
        # Verifica che il file sia un PDF valido
        with open(output_path, 'rb') as f:
            content = f.read(1024)
            assert content.startswith(b'%PDF')
    
    def test_pdf_with_missing_data(self):
        """Test PDF con dati mancanti"""
        incomplete_data = {
            "video_title": "Video Incompleto",
            "overall_score": 50
        }
        
        output_path = os.path.join(self.temp_dir, "incomplete.pdf")
        result_path = export_analysis_to_pdf(incomplete_data, output_path)
        
        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 500

@pytest.mark.skipif(not PRO_FEATURES_AVAILABLE, reason="Funzionalità Pro non disponibili")
class TestDatabase:
    """Test per il sistema database"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_url = f"sqlite:///{self.temp_db.name}"
        self.db_manager = init_database(self.db_url)
    
    def teardown_method(self):
        """Cleanup dopo ogni test"""
        self.temp_db.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test inizializzazione database"""
        assert self.db_manager is not None
        assert hasattr(self.db_manager, 'engine')
        assert hasattr(self.db_manager, 'SessionLocal')
    
    def test_create_user(self):
        """Test creazione utente"""
        user = self.db_manager.create_user(
            username="test_user",
            email="test@example.com",
            password_hash="hash123"
        )
        
        assert user.id is not None
        assert user.username == "test_user"
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_save_video_analysis(self):
        """Test salvataggio analisi video"""
        # Crea utente prima
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        
        analysis_data = {
            "video_title": "Test Video",
            "overall_score": 85.5,
            "summary": "Video di test",
            "keywords": ["test", "video"],
            "metrics": {
                "engagement_rate": 4.2,
                "completion_rate": 75
            }
        }
        
        analysis = self.db_manager.save_video_analysis(user.id, analysis_data)
        
        assert analysis.id is not None
        assert analysis.video_title == "Test Video"
        assert analysis.overall_score == 85.5
        assert analysis.user_id == user.id
    
    def test_save_agent_insight(self):
        """Test salvataggio insight agente"""
        # Crea utente e analisi prima
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        analysis = self.db_manager.save_video_analysis(user.id, {"video_title": "Test", "overall_score": 80})
        
        agent_data = {
            "agent_type": "strategist",
            "agent_name": "[TARGET] Strategist",
            "agent_role": "Esperto strategia",
            "message": "Test insight",
            "response_type": "advice",
            "confidence_score": 0.9
        }
        
        insight = self.db_manager.save_agent_insight(user.id, analysis.id, agent_data)
        
        assert insight.id is not None
        assert insight.agent_type == "strategist"
        assert insight.message == "Test insight"
        assert insight.video_analysis_id == analysis.id
    
    def test_get_user_analyses(self):
        """Test recupero analisi utente"""
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        
        # Crea alcune analisi
        for i in range(3):
            self.db_manager.save_video_analysis(user.id, {
                "video_title": f"Video {i}",
                "overall_score": 70 + i * 5
            })
        
        analyses = self.db_manager.get_user_analyses(user.id, limit=5)
        
        assert len(analyses) == 3
        assert all(analysis.user_id == user.id for analysis in analyses)
    
    def test_get_analysis_by_id(self):
        """Test recupero analisi per ID"""
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        analysis = self.db_manager.save_video_analysis(user.id, {
            "video_title": "Test Video",
            "overall_score": 85
        })
        
        retrieved = self.db_manager.get_analysis_by_id(analysis.id)
        
        assert retrieved is not None
        assert retrieved.id == analysis.id
        assert retrieved.video_title == "Test Video"
    
    def test_get_analytics_summary(self):
        """Test riepilogo analytics"""
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        
        # Crea analisi con keywords
        for i in range(2):
            self.db_manager.save_video_analysis(user.id, {
                "video_title": f"Video {i}",
                "overall_score": 80,
                "keywords": ["tiktok", "viral", "content"]
            })
        
        summary = self.db_manager.get_analytics_summary(user.id, days=30)
        
        assert summary["total_analyses"] == 2
        assert summary["average_score"] > 0
        assert len(summary["top_keywords"]) > 0

@pytest.mark.skipif(not PRO_FEATURES_AVAILABLE, reason="Funzionalità Pro non disponibili")
class TestIntegration:
    """Test di integrazione tra i moduli"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_url = f"sqlite:///{self.temp_db.name}"
        self.db_manager = init_database(self.db_url)
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup dopo ogni test"""
        self.temp_db.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test workflow completo: analisi -> database -> PDF"""
        # 1. Crea utente
        user = self.db_manager.create_user("test_user", "test@example.com", "hash123")
        
        # 2. Salva analisi
        analysis_data = {
            "video_title": "Workflow Test Video",
            "overall_score": 88.5,
            "summary": "Test del workflow completo",
            "keywords": ["workflow", "test", "integration"],
            "metrics": {"engagement_rate": 4.5}
        }
        
        analysis = self.db_manager.save_video_analysis(user.id, analysis_data)
        
        # 3. Salva insight agente
        chat = AgentChat()
        agent_response = chat.get_agent_response("strategist", "Analizza questo video")
        
        agent_data = {
            "agent_type": "strategist",
            "agent_name": "[TARGET] Strategist",
            "agent_role": "Esperto strategia",
            "message": agent_response,
            "response_type": "analysis"
        }
        
        insight = self.db_manager.save_agent_insight(user.id, analysis.id, agent_data)
        
        # 4. Genera PDF
        pdf_data = {
            "video_title": analysis.video_title,
            "overall_score": analysis.overall_score,
            "summary": analysis.summary,
            "keywords": analysis.keywords,
            "metrics": {"engagement_rate": 4.5},
            "recommendations": [
                {
                    "title": "Test Recommendation",
                    "description": "Test del workflow completo"
                }
            ]
        }
        
        pdf_path = os.path.join(self.temp_dir, "workflow_test.pdf")
        result_pdf = export_analysis_to_pdf(pdf_data, pdf_path)
        
        # Verifiche
        assert analysis.id is not None
        assert insight.id is not None
        assert os.path.exists(result_pdf)
        assert len(agent_response) > 10
    
    def test_error_handling(self):
        """Test gestione errori"""
        # Test con dati invalidi
        with pytest.raises(Exception):
            export_analysis_to_pdf({}, "invalid/path/file.pdf")
        
        # Test database con dati mancanti
        with pytest.raises(Exception):
            self.db_manager.save_video_analysis(999, {})  # User non esistente

def test_pro_features_availability():
    """Test disponibilità funzionalità Pro"""
    if PRO_FEATURES_AVAILABLE:
        assert True  # Funzionalità disponibili
    else:
        pytest.skip("Funzionalità Pro non installate")

if __name__ == "__main__":
    # Esegui test se chiamato direttamente
    pytest.main([__file__, "-v"]) 