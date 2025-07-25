#!/usr/bin/env python3
"""
TokIntel v2 - Video Analysis Pipeline
Orchestrates all analysis agents for video processing
"""

from typing import Dict, List, Any, Optional
import logging
logger = logging.getLogger(__name__)
import asyncio

from core.logger import setup_logger
from core.exceptions import PipelineError
from agent.scraper import ScraperAgent
from agent.synthesis import SynthesisAgent
from agent.devika_team import DevikaAgentTeam

logger = setup_logger(__name__)

class VideoAnalysisPipeline:
    """Main pipeline for video analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize pipeline with configuration"""
        self.config = config
        self.logger = logger
        
        # Initialize agents
        self.scraper = ScraperAgent()
        self.synthesis = SynthesisAgent()
        self.devika_team = DevikaAgentTeam(config)
        
        self.logger.info("Video analysis pipeline initialized")
    
    async def analyze(self, video_path: str) -> Dict[str, Any]:
        """Analyze a video file through the complete pipeline"""
        try:
            self.logger.info(f"Starting analysis pipeline for: {video_path}")
            
            # Step 1: Extract frames
            self.logger.debug("Step 1: Extracting frames")
            frames = await self._extract_frames(video_path)
            
            # Step 2: Extract text from frames (OCR)
            self.logger.debug("Step 2: Extracting text from frames")
            ocr_text = await self._extract_text(frames)
            
            # Step 3: Transcribe audio
            self.logger.debug("Step 3: Transcribing audio")
            transcript = await self._transcribe_audio(video_path)
            
            # Step 4: Generate summary
            self.logger.debug("Step 4: Generating summary")
            summary = await self._generate_summary(transcript, ocr_text)
            
            # Step 5: Evaluate and score
            self.logger.debug("Step 5: Evaluating and scoring")
            score = await self._evaluate_content(summary, transcript, ocr_text)
            
            # Step 6: Devika Team Analysis
            self.logger.debug("Step 6: Running Devika team analysis")
            devika_analysis = await self._run_devika_analysis(transcript, ocr_text, summary)
            
            # Step 7: Export results
            self.logger.debug("Step 7: Exporting results")
            await self._export_results(video_path, summary, score, devika_analysis)
            
            # Compile results
            results = {
                "video_path": video_path,
                "summary": summary,
                "score": score,
                "transcript": transcript,
                "ocr_text": ocr_text,
                "frame_count": len(frames) if frames else 0,
                "devika_analysis": devika_analysis
            }
            
            self.logger.info(f"Analysis completed successfully for: {video_path}")
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline analysis failed for {video_path}: {e}")
            raise PipelineError(f"Analysis failed: {e}")
    
    async def _extract_frames(self, video_path: str) -> List:
        """Extract frames from video"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            frames = await loop.run_in_executor(
                None, self.scraper.extract_frames, video_path
            )
            self.logger.debug(f"Extracted {len(frames)} frames")
            return frames
        except Exception as e:
            self.logger.error(f"Frame extraction failed: {e}")
            raise PipelineError(f"Frame extraction failed: {e}")
    
    async def _extract_text(self, frames: List) -> str:
        """Extract text from frames using OCR"""
        try:
            if not frames:
                self.logger.warning("No frames to extract text from")
                return ""
            
            # Placeholder for OCR functionality
            # TODO: Implement OCR text extraction
            self.logger.debug("OCR text extraction not implemented yet")
            return ""
        except Exception as e:
            self.logger.error(f"OCR text extraction failed: {e}")
            raise PipelineError(f"OCR text extraction failed: {e}")
    
    async def _transcribe_audio(self, video_path: str) -> str:
        """Transcribe audio from video"""
        try:
            # Placeholder for audio transcription functionality
            # TODO: Implement audio transcription
            self.logger.debug("Audio transcription not implemented yet")
            return ""
        except Exception as e:
            self.logger.error(f"Audio transcription failed: {e}")
            raise PipelineError(f"Audio transcription failed: {e}")
    
    async def _generate_summary(self, transcript: str, ocr_text: str) -> str:
        """Generate summary from transcript and OCR text"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            summary = await loop.run_in_executor(
                None, self.synthesis.summarize, transcript, ocr_text, self.config
            )
            self.logger.debug(f"Generated summary: {len(summary)} characters")
            return summary
        except Exception as e:
            self.logger.error(f"Summary generation failed: {e}")
            raise PipelineError(f"Summary generation failed: {e}")
    
    async def _evaluate_content(self, summary: str, transcript: str, ocr_text: str) -> Dict[str, Any]:
        """Evaluate and score the content"""
        try:
            # Placeholder for content evaluation functionality
            # TODO: Implement content evaluation
            self.logger.debug("Content evaluation not implemented yet")
            return {"score": 0, "details": "Evaluation not implemented"}
        except Exception as e:
            self.logger.error(f"Content evaluation failed: {e}")
            raise PipelineError(f"Content evaluation failed: {e}")
    
    async def _run_devika_analysis(self, transcript: str, ocr_text: str, summary: str) -> dict:
        """Run Devika team analysis on content and return a serializable dict"""
        try:
            # Combina tutto il contenuto per l'analisi
            combined_content = f"{transcript}\n\n{ocr_text}\n\n{summary}"
            
            # Prepara metadati
            metadata = {
                'title': f'Video Analysis - {len(transcript)} chars',
                'has_ocr': bool(ocr_text.strip()),
                'has_transcript': bool(transcript.strip()),
                'content_length': len(combined_content)
            }
            
            # Esegui analisi del team
            devika_result = await self.devika_team.run_team_analysis(combined_content, metadata)
            
            # Se è una dataclass, converti in dict serializzabile
            if hasattr(devika_result, '__dataclass_fields__'):
                from agent.devika_team import run_devika_team_analysis
                # Usiamo la funzione utility per serializzare
                serializable = await run_devika_team_analysis(combined_content, self.config)
                return serializable
            return devika_result
        except Exception as e:
            self.logger.error(f"Devika analysis failed: {e}")
            # Fallback: ritorna analisi base
            return {
                'video_title': 'Video Analysis',
                'overall_score': 0.5,
                'viral_potential': 0.5,
                'engagement_prediction': 0.5,
                'agent_analyses': [],
                'team_recommendations': ['Analisi non disponibile'],
                'priority_actions': ['Riprova l\'analisi'],
                'timestamp': None
            }
    
    async def _export_results(self, video_path: str, summary: str, score: Dict[str, Any], devika_analysis: Dict[str, Any]):
        """Export analysis results"""
        try:
            # Placeholder for export functionality
            # TODO: Implement results export
            self.logger.debug("Results export not implemented yet")
        except Exception as e:
            self.logger.error(f"Results export failed: {e}")
            # Don't raise here as export failure shouldn't fail the entire pipeline
            self.logger.warning("Continuing without export")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            "config": self.config,
            "agents_initialized": True,
            "pipeline_ready": True
        } 