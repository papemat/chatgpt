#!/usr/bin/env python3
"""
TokIntel v2 - Custom Exceptions
Custom exception classes for TokIntel application
"""

class TokIntelError(Exception):
    """Base exception for TokIntel application"""
    pass

class ConfigurationError(TokIntelError):
    """Raised when there's a configuration error"""
    pass

class VideoProcessingError(TokIntelError):
    """Raised when there's an error processing video files"""
    pass

class LLMError(TokIntelError):
    """Raised when there's an error with LLM operations"""
    pass

class FileValidationError(TokIntelError):
    """Raised when file validation fails"""
    pass

class ExportError(TokIntelError):
    """Raised when there's an error exporting results"""
    pass

class PipelineError(TokIntelError):
    """Raised when there's an error in the analysis pipeline"""
    pass 