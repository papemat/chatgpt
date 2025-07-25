"""
Unit tests for configuration module
"""

from typing import Dict, List, Any, Optional
import pytest
import tempfile
import os


class TestTokIntelConfig:
    """Test TokIntelConfig validation"""
    
    def test_default_config(self):
        """Test default configuration creation"""
        config = TokIntelConfig()
        assert config.model == "gpt-4"
        assert config.language == "it"
        assert len(config.keywords) > 0
        assert config.output_folder == "output/"
    
    def test_custom_config(self):
        """Test custom configuration creation"""
        config = TokIntelConfig(
            model="gpt-3.5-turbo",
            language="en",
            keywords=["test", "keyword"],
            output_folder="custom_output/"
        )
        assert config.model == "gpt-3.5-turbo"
        assert config.language == "en"
        assert config.keywords == ["test", "keyword"]
        assert config.output_folder == "custom_output/"
    
    def test_invalid_language(self):
        """Test invalid language validation"""
        with pytest.raises(ValueError, match="Invalid language"):
            TokIntelConfig(language="invalid")
    
    def test_invalid_export_format(self):
        """Test invalid export format validation"""
        with pytest.raises(ValueError, match="Invalid export format"):
            TokIntelConfig(export_format=["invalid"])
    
    def test_invalid_log_level(self):
        """Test invalid log level validation"""
        with pytest.raises(ValueError, match="Invalid log level"):
            TokIntelConfig(log_level="invalid")


class TestLLMConfig:
    """Test LLMConfig validation"""
    
    def test_default_llm_config(self):
        """Test default LLM configuration"""
        config = LLMConfig()
        assert config.model == "gpt-4"
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.temperature == 0.7
        assert config.max_tokens == 500
    
    def test_custom_llm_config(self):
        """Test custom LLM configuration"""
        config = LLMConfig(
            model="gpt-3.5-turbo",
            endpoint="http://localhost:1234",
            api_key="test-key",
            timeout=60,
            max_retries=5,
            temperature=0.5,
            max_tokens=1000
        )
        assert config.model == "gpt-3.5-turbo"
        assert config.endpoint == "http://localhost:1234"
        assert config.api_key == "test-key"
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.temperature == 0.5
        assert config.max_tokens == 1000


class TestWeightsConfig:
    """Test WeightsConfig validation"""
    
    def test_default_weights(self):
        """Test default weights configuration"""
        weights = WeightsConfig()
        assert weights.keywords == 1.5
        assert weights.speech_density == 1.0
        assert weights.ocr == 1.2
        assert weights.engagement == 1.0
        assert weights.viral_potential == 1.3


class TestConfigManager:
    """Test ConfigManager functionality"""
    
    def test_load_default_config(self):
        """Test loading default configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            config = manager.get_config()
            assert "model" in config
            assert "language" in config
            assert "keywords" in config
    
    def test_load_from_file(self):
        """Test loading configuration from file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            
            # Create test config file
            config_content = """
model: "gpt-3.5-turbo"
language: "en"
keywords:
  - "test"
  - "keyword"
output_folder: "test_output/"
llm_config:
  model: "gpt-3.5-turbo"
  timeout: 60
"""
            config_path.write_text(config_content)
            
            manager = ConfigManager(str(config_path))
            config = manager.get_config()
            
            assert config["model"] == "gpt-3.5-turbo"
            assert config["language"] == "en"
            assert config["keywords"] == ["test", "keyword"]
            assert config["output_folder"] == "test_output/"
            assert config["llm_config"]["timeout"] == 60
    
    def test_environment_variables(self):
        """Test environment variable override"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            
            # Set environment variables
            os.environ["TOKINTEL_MODEL"] = "gpt-3.5-turbo"
            os.environ["TOKINTEL_LANGUAGE"] = "en"
            os.environ["TOKINTEL_LLM_TIMEOUT"] = "45"
            
            try:
                manager = ConfigManager(str(config_path))
                config = manager.get_config()
                
                assert config["model"] == "gpt-3.5-turbo"
                assert config["language"] == "en"
                assert config["llm_config"]["timeout"] == 45
            finally:
                # Clean up environment variables
                for key in ["TOKINTEL_MODEL", "TOKINTEL_LANGUAGE", "TOKINTEL_LLM_TIMEOUT"]:
                    os.environ.pop(key, None)
    
    def test_update_config(self):
        """Test configuration updates"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            # Update configuration
            updates = {
                "model": "gpt-3.5-turbo",
                "language": "en",
                "keywords": ["new", "keywords"]
            }
            manager.update_config(updates)
            
            config = manager.get_config()
            assert config["model"] == "gpt-3.5-turbo"
            assert config["language"] == "en"
            assert config["keywords"] == ["new", "keywords"]
    
    def test_save_config(self):
        """Test saving configuration to file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            # Update and save configuration
            manager.update_config({"model": "gpt-3.5-turbo"})
            manager.save_config()
            
            # Verify file was created
            assert config_path.exists()
            
            # Load and verify content
            content = config_path.read_text()
            assert "gpt-3.5-turbo" in content
    
    def test_get_llm_config(self):
        """Test getting LLM-specific configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            llm_config = manager.get_llm_config()
            assert "model" in llm_config
            assert "timeout" in llm_config
            assert "max_retries" in llm_config
    
    def test_validate_config(self):
        """Test configuration validation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            # Should pass validation
            assert manager.validate_config() is True
    
    def test_get_config_summary(self):
        """Test getting configuration summary"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            manager = ConfigManager(str(config_path))
            
            summary = manager.get_config_summary()
            assert "model" in summary
            assert "language" in summary
            assert "keywords_count" in summary
            assert "output_folder" in summary 