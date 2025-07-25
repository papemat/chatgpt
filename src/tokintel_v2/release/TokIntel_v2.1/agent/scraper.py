#!/usr/bin/env python3
"""
TokIntel v2 - Scraper Agent
Extracts frames from video files for analysis
"""

from typing import Dict, List, Any, Optional
import cv2
import os
import asyncio
import time
from core.logger import LoggerMixin
from core.exceptions import VideoProcessingError

def async_retry(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    """Decorator for async retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            delay = base_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        await asyncio.sleep(delay)
                        delay = min(delay * 2, max_delay)
                    else:
                        raise last_exception
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class ScraperAgent(LoggerMixin):
    """Agent responsible for extracting frames from video files"""
    
    def __init__(self, every_n_frames: int = 30, max_retries: int = 3):
        """Initialize scraper agent"""
        super().__init__()
        self.every_n_frames = every_n_frames
        self.max_retries = max_retries
        self.log_info("ScraperAgent initialized with async support")
    
    async def extract_frames(self, video_path: str, every_n_frames: Optional[int] = None) -> List:
        """Extract frames from video file asynchronously"""
        start_time = time.time()
        self.log_info(f"[INFO] Starting frame extraction from: {video_path}")
        
        try:
            if every_n_frames is None:
                every_n_frames = self.every_n_frames
            
            # Run the actual extraction in a thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            frames = await loop.run_in_executor(
                None, 
                self._extract_frames_sync, 
                video_path, 
                every_n_frames
            )
            
            end_time = time.time()
            duration = end_time - start_time
            self.log_info(f"[OK] Frame extraction completed: {len(frames)} frames in {duration:.2f}s")
            return frames
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.log_error(f"[ERROR] Frame extraction failed after {duration:.2f}s: {e}", exc_info=True)
            raise VideoProcessingError(f"Frame extraction failed: {e}")
    
    def _extract_frames_sync(self, video_path: str, every_n_frames: int) -> List:
        """Synchronous frame extraction (runs in thread pool)"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise VideoProcessingError(f"Cannot open video file: {video_path}")
        
        frames = []
        count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if count % every_n_frames == 0:
                    frames.append(frame)
                    # Log progress every 100 frames
                    if len(frames) % 100 == 0:
                        progress = (count / total_frames) * 100 if total_frames > 0 else 0
                        self.log_info(f"[REPORT] Extraction progress: {progress:.1f}% ({len(frames)} frames)")
                
                count += 1
                
                # Yield control periodically to avoid blocking
                if count % 1000 == 0:
                    time.sleep(0.001)
            
            return frames
            
        finally:
            cap.release()
    
    @async_retry(max_retries=3)
    async def extract_frames_with_timestamps(self, video_path: str, every_n_frames: Optional[int] = None) -> List[Tuple]:
        """Extract frames with their timestamps asynchronously with retry logic"""
        start_time = time.time()
        self.log_info(f"[INFO] Starting timestamped frame extraction from: {video_path}")
        
        try:
            if every_n_frames is None:
                every_n_frames = self.every_n_frames
            
            # Run the actual extraction in a thread pool
            loop = asyncio.get_running_loop()
            frames_with_timestamps = await loop.run_in_executor(
                None, 
                self._extract_frames_with_timestamps_sync, 
                video_path, 
                every_n_frames
            )
            
            end_time = time.time()
            duration = end_time - start_time
            self.log_info(f"[OK] Timestamped extraction completed: {len(frames_with_timestamps)} frames in {duration:.2f}s")
            return frames_with_timestamps
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.log_error(f"[ERROR] Timestamped extraction failed after {duration:.2f}s: {e}", exc_info=True)
            raise VideoProcessingError(f"Frame extraction with timestamps failed: {e}")
    
    def _extract_frames_with_timestamps_sync(self, video_path: str, every_n_frames: int) -> List[Tuple]:
        """Synchronous timestamped frame extraction (runs in thread pool)"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise VideoProcessingError(f"Cannot open video file: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames_with_timestamps = []
        count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if count % every_n_frames == 0:
                    timestamp = count / fps if fps > 0 else 0
                    frames_with_timestamps.append((frame, timestamp))
                    
                    # Log progress every 100 frames
                    if len(frames_with_timestamps) % 100 == 0:
                        progress = (count / total_frames) * 100 if total_frames > 0 else 0
                        self.log_info(f"[REPORT] Timestamped extraction progress: {progress:.1f}% ({len(frames_with_timestamps)} frames)")
                
                count += 1
                
                # Yield control periodically
                if count % 1000 == 0:
                    time.sleep(0.001)
            
            return frames_with_timestamps
            
        finally:
            cap.release()
    
    @async_retry(max_retries=3)
    async def get_video_info(self, video_path: str) -> dict:
        """Get basic video information asynchronously with retry logic"""
        start_time = time.time()
        self.log_info(f"[INFO] Getting video info for: {video_path}")
        
        try:
            # Run video info extraction in thread pool
            loop = asyncio.get_running_loop()
            video_info = await loop.run_in_executor(
                None, 
                self._get_video_info_sync, 
                video_path
            )
            
            end_time = time.time()
            duration = end_time - start_time
            self.log_info(f"[OK] Video info retrieved in {duration:.2f}s: {video_info['frame_count']} frames, {video_info['duration']:.1f}s duration")
            return video_info
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.log_error(f"[ERROR] Failed to get video info after {duration:.2f}s: {e}", exc_info=True)
            raise VideoProcessingError(f"Failed to get video info: {e}")
    
    def _get_video_info_sync(self, video_path: str) -> dict:
        """Synchronous video info extraction (runs in thread pool)"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise VideoProcessingError(f"Cannot open video file: {video_path}")
        
        try:
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            return {
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height,
                "duration": duration
            }
            
        finally:
            cap.release()
    
    async def batch_extract_frames(self, video_paths: List[str], every_n_frames: Optional[int] = None) -> dict:
        """Extract frames from multiple videos concurrently"""
        start_time = time.time()
        self.log_info(f"[INFO] Starting batch extraction for {len(video_paths)} videos")
        
        try:
            # Create tasks for concurrent execution
            tasks = [
                self.extract_frames(video_path, every_n_frames) 
                for video_path in video_paths
            ]
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            successful_results = {}
            failed_results = {}
            
            for video_path, result in zip(video_paths, results):
                if isinstance(result, Exception):
                    failed_results[video_path] = str(result)
                    self.log_error(f"[ERROR] Failed to extract frames from {video_path}: {result}")
                else:
                    successful_results[video_path] = result
                    self.log_info(f"[OK] Successfully extracted {len(result)} frames from {video_path}")
            
            end_time = time.time()
            duration = end_time - start_time
            self.log_info(f"[OK] Batch extraction completed in {duration:.2f}s: {len(successful_results)} successful, {len(failed_results)} failed")
            
            return {
                "successful": successful_results,
                "failed": failed_results,
                "total_duration": duration
            }
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.log_error(f"[ERROR] Batch extraction failed after {duration:.2f}s: {e}", exc_info=True)
            raise VideoProcessingError(f"Batch extraction failed: {e}")
