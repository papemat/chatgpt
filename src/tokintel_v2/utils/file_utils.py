#!/usr/bin/env python3
"""
TokIntel v2 - File Utilities
File validation and video file discovery utilities
"""

from typing import Dict, List, Any, Optional
import cv2
import re

# Supported video formats
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}

def validate_video_file(file_path: str) -> bool:
    """Validate if a file is a supported video file"""
    try:
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            raise FileValidationError(f"File does not exist: {file_path}")
        
        # Check file extension
        if file_path.suffix.lower() not in SUPPORTED_VIDEO_FORMATS:
            raise FileValidationError(f"Unsupported video format: {file_path.suffix}")
        
        # Check if file is readable with OpenCV
        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            raise FileValidationError(f"Cannot open video file: {file_path}")
        
        # Check if video has frames
        ret, _ = cap.read()
        if not ret:
            raise FileValidationError(f"Video file has no readable frames: {file_path}")
        
        cap.release()
        return True
        
    except Exception as e:
        if isinstance(e, FileValidationError):
            raise
        raise FileValidationError(f"Error validating video file {file_path}: {e}")

def get_video_files(directory: str) -> List[str]:
    """Get all video files from a directory"""
    try:
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileValidationError(f"Directory does not exist: {directory}")
        
        if not dir_path.is_dir():
            raise FileValidationError(f"Path is not a directory: {directory}")
        
        video_files = []
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_VIDEO_FORMATS:
                video_files.append(str(file_path))
        
        return sorted(video_files)
        
    except Exception as e:
        if isinstance(e, FileValidationError):
            raise
        raise FileValidationError(f"Error getting video files from {directory}: {e}")

def get_video_info(file_path: str) -> dict:
    """Get basic information about a video file"""
    try:
        cap = cv2.VideoCapture(file_path)
        
        if not cap.isOpened():
            raise FileValidationError(f"Cannot open video file: {file_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate duration
        duration = frame_count / fps if fps > 0 else 0
        
        cap.release()
        
        return {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration": duration,
            "file_size": Path(file_path).stat().st_size
        }
        
    except Exception as e:
        raise FileValidationError(f"Error getting video info for {file_path}: {e}")

def create_output_directory(output_path: str) -> Path:
    """Create output directory if it doesn't exist"""
    try:
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    except Exception as e:
        raise FileValidationError(f"Error creating output directory {output_path}: {e}")

def get_safe_filename(filename: str) -> str:
    """Convert filename to a safe version for file systems"""
    # Remove or replace unsafe characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    safe_filename = safe_filename.strip('. ')
    
    # Ensure filename is not empty
    if not safe_filename:
        safe_filename = "unnamed_file"
    
    return safe_filename 