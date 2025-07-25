#!/usr/bin/env python3
"""
TokIntel v2 - Configuration Manager
Handles loading and managing configuration from YAML files with validation
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
import yaml
import os
from pathlib import Path
from pydantic import BaseModel, Field, validator

# Setup basic logging
logger = logging.getLogger(__name__)

class LLMConfig(BaseModel):
    """LLM configuration model"""
    model: str = Field(default="gpt-4", description="LLM model to use")
    endpoint: Optional[str] = Field(default=None, description="Local LLM endpoint")
    api_key: Optional[str] = Field(default=None, description="API key for remote LLM")
    timeout: int = Field(default=30, ge=1, le=300, description="Request timeout in seconds")
    max_retries: int = Field(default=3, ge=0, le=10, description="Maximum retry attempts")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: int = Field(default=500, ge=1, le=4000, description="Maximum tokens per response")

class WeightsConfig(BaseModel):
    """Analysis weights configuration"""
    keywords: float = Field(default=1.5, ge=0.0, le=10.0)
    speech_density: float = Field(default=1.0, ge=0.0, le=10.0)
    ocr: float = Field(default=1.2, ge=0.0, le=10.0)
    engagement: float = Field(default=1.0, ge=0.0, le=10.0)
    viral_potential: float = Field(default=1.3, ge=0.0, le=10.0)

class TokIntelConfig(BaseModel):
    """Main TokIntel configuration model"""
    # Basic settings
    model: str = Field(default="gpt-4", description="Default LLM model")
    language: str = Field(default="it", description="Analysis language")
    
    # Analysis settings
    keywords: List[str] = Field(
        default=["motivazione", "hook", "viral", "emozione"],
        description="Target keywords for analysis"
    )
    weights: WeightsConfig = Field(default_factory=WeightsConfig)
    
    # Output settings
    export_format: List[str] = Field(
        default=["csv", "json"],
        description="Export formats"
    )
    output_folder: str = Field(default="output/", description="Output directory")
    
    # LLM settings
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    
    # Processing settings
    frame_extraction_interval: int = Field(default=30, ge=1, le=300)
    max_video_duration: int = Field(default=300, ge=1, le=3600)  # 5 minutes default
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    log_rotation_enabled: bool = Field(default=True, description="Enable log rotation")
    log_max_bytes: int = Field(default=10485760, ge=1024, le=104857600, description="Max log file size in bytes (default 10MB)")
    log_backup_count: int = Field(default=5, ge=1, le=100, description="Number of rotated log files to keep")
    
    @validator('export_format')
    def validate_export_format(cls, v):
        """Validate export formats"""
        valid_formats = ['csv', 'json', 'xlsx', 'txt']
        for fmt in v:
            if fmt not in valid_formats:
                raise ValueError(f"Invalid export format: {fmt}. Valid formats: {valid_formats}")
        return v
    
    @validator('language')
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ['it', 'en', 'es', 'fr', 'de']
        if v not in valid_languages:
            raise ValueError(f"Invalid language: {v}. Valid languages: {valid_languages}")
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Valid levels: {valid_levels}")
        return v.upper()

class ConfigManager:
    """Manages TokIntel configuration with validation and environment support"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize configuration manager"""
        self.config_path = Path(config_path)
        self._config = None
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file with environment variable support"""
        try:
            logger.info(f"Loading configuration from: {self.config_path}")
            
            # Load from file if exists
            file_config = {}
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f) or {}
                logger.debug("Configuration loaded from file")
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
            
            # Override with environment variables
            env_config = self._load_env_config()
            
            # Merge configurations (env overrides file)
            merged_config = self._merge_configs(file_config, env_config)
            
            # Validate and create config object
            self._config = TokIntelConfig(**merged_config)
            
            logger.info("Configuration loaded and validated successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise ValueError(f"Configuration error: {e}")
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        env_config = {}
        
        # Map environment variables to config keys
        env_mapping = {
            'TOKINTEL_MODEL': 'model',
            'TOKINTEL_LANGUAGE': 'language',
            'TOKINTEL_OUTPUT_FOLDER': 'output_folder',
            'TOKINTEL_LOG_LEVEL': 'log_level',
            'TOKINTEL_LOG_FILE': 'log_file',
            'TOKINTEL_LLM_ENDPOINT': 'llm_config.endpoint',
            'TOKINTEL_LLM_API_KEY': 'llm_config.api_key',
            'TOKINTEL_LLM_TIMEOUT': 'llm_config.timeout',
            'TOKINTEL_LLM_MAX_RETRIES': 'llm_config.max_retries',
            'TOKINTEL_FRAME_INTERVAL': 'frame_extraction_interval',
            'TOKINTEL_MAX_DURATION': 'max_video_duration'
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Handle nested keys
                if '.' in config_key:
                    parent, child = config_key.split('.')
                    if parent not in env_config:
                        env_config[parent] = {}
                    env_config[parent][child] = value
                else:
                    env_config[config_key] = value
        
        if env_config:
            logger.debug(f"Loaded {len(env_config)} environment variables")
        
        return env_config
    
    def _merge_configs(self, file_config: Dict[str, Any], env_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge file and environment configurations"""
        merged = file_config.copy()
        
        # Merge environment config (overrides file config)
        for key, value in env_config.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key].update(value)
            else:
                merged[key] = value
        
        return merged
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration as dictionary"""
        return self._config.dict()
    
    def get_config_object(self) -> TokIntelConfig:
        """Get current configuration object"""
        return self._config
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        try:
            # Create new config with updates
            current_dict = self._config.dict()
            current_dict.update(updates)
            
            # Validate new configuration
            self._config = TokIntelConfig(**current_dict)
            logger.info("Configuration updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            raise ValueError(f"Configuration update failed: {e}")
    
    def save_config(self, config_path: Optional[str] = None):
        """Save current configuration to file"""
        try:
            save_path = Path(config_path) if config_path else self.config_path
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dict and save
            config_dict = self._config.dict()
            
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.info(f"Configuration saved to: {save_path}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise ValueError(f"Configuration save failed: {e}")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM-specific configuration"""
        return self._config.llm_config.dict()
    
    def validate_config(self) -> bool:
        """Validate current configuration"""
        try:
            # Pydantic validation is automatic, but we can add custom validation here
            if not self._config.keywords:
                logger.warning("No keywords configured for analysis")
            
            if not self._config.llm_config.api_key and not self._config.llm_config.endpoint:
                logger.warning("No LLM API key or endpoint configured")
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for logging"""
        return {
            "model": self._config.model,
            "language": self._config.language,
            "keywords_count": len(self._config.keywords),
            "output_folder": self._config.output_folder,
            "export_formats": self._config.export_format,
            "llm_endpoint": self._config.llm_config.endpoint is not None,
            "llm_api_key": self._config.llm_config.api_key is not None
        } 