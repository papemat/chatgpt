"""
Audio processing module for TokIntel
"""

from typing import Dict, List, Any, Optional
from .whisper_transcriber import WhisperTranscriber, create_transcriber

__all__ = ['WhisperTranscriber', 'create_transcriber'] 