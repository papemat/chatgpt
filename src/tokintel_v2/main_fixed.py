#!/usr/bin/env python3
"""
TokIntel v2 - Main Entry Point (Fixed Version)
Analizzatore modulare di video TikTok con architettura scalabile
"""

from typing import Dict, List, Any, Optional
import logging
logger = logging.getLogger(__name__)
import os
import sys
import argparse
import asyncio

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from core.config import ConfigManager
from core.logger import setup_logger
from core.exceptions import TokIntelError
from ui.streamlit_launcher import StreamlitLauncher

# Setup logging
logger = setup_logger(__name__)

class TokIntelCore:
    """Core processing class for TokIntel video analysis"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize TokIntel core with configuration"""
        logger.info("Initializing TokIntel core...")
        try:
            self.config_manager = ConfigManager(config_path)
            self.config = self.config_manager.get_config()
            self.pipeline = VideoAnalysisPipeline(self.config)
            logger.info("TokIntel core initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TokIntel core: {e}")
            raise TokIntelError(f"Configuration error: {e}")
    
    async def process_video(self, video_path: str) -> Dict[str, Any]:
        """Process a single video file"""
        logger.info(f"Starting analysis of video: {video_path}")
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Validate video file
            if not validate_video_file(video_path):
                raise TokIntelError(f"Invalid video file: {video_path}")
            
            # Process video through pipeline
            results = await self.pipeline.analyze(video_path)
            
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.info(f"Successfully analyzed video: {video_path} in {processing_time:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Error processing video {video_path}: {e}")
            raise TokIntelError(f"Processing error: {e}")
    
    async def process_directory(self, input_dir: str) -> List[Dict[str, Any]]:
        """Process all video files in a directory"""
        logger.info(f"Processing directory: {input_dir}")
        
        video_files = get_video_files(input_dir)
        if not video_files:
            logger.warning(f"No video files found in: {input_dir}")
            return []
        
        logger.info(f"Found {len(video_files)} video files to process")
        
        results = []
        for i, video_file in enumerate(video_files, 1):
            try:
                logger.info(f"Processing {i}/{len(video_files)}: {video_file}")
                result = await self.process_video(video_file)
                results.append(result)
            except TokIntelError as e:
                logger.error(f"Skipping {video_file}: {e}")
                continue
        
        logger.info(f"Completed processing {len(results)} videos")
        return results
    
    def run_sync(self, input_path: str) -> List[Dict[str, Any]]:
        """Synchronous wrapper for async processing"""
        return asyncio.run(self.process_directory(input_path))
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self.config.update(updates)
        logger.info("Configuration updated")

class TokIntelCLI:
    """CLI interface for TokIntel"""
    
    def __init__(self):
        """Initialize CLI interface"""
        self.core = None
    
    def setup_arguments(self) -> argparse.Namespace:
        """Setup command line arguments"""
        parser = argparse.ArgumentParser(
            description="TokIntel v2 - Analizzatore Video TikTok",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Esempi di utilizzo:
  python main.py --input demo_input/
  python main.py --input video.mp4 --config custom_config.yaml
  python main.py --input /path/to/videos --output results/
  python main.py --ui  # Avvia interfaccia Streamlit
        """
        )
        
        parser.add_argument(
            "--input", "-i",
            help="Percorso al file video o directory di video"
        )
        
        parser.add_argument(
            "--config", "-c",
            default="config/config.yaml",
            help="Percorso al file di configurazione (default: config/config.yaml)"
        )
        
        parser.add_argument(
            "--output", "-o",
            default="output/",
            help="Directory di output per i risultati (default: output/)"
        )
        
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Abilita logging dettagliato"
        )
        
        parser.add_argument(
            "--ui", "--streamlit",
            action="store_true",
            help="Avvia interfaccia Streamlit"
        )
        
        parser.add_argument(
            "--model",
            help="Modello LLM da utilizzare (override configurazione)"
        )
        
        parser.add_argument(
            "--language",
            help="Lingua per l'analisi (override configurazione)"
        )
        
        return parser.parse_args()
    
    def run(self):
        """Main CLI execution"""
        logger.info("Starting TokIntel CLI...")
        args = self.setup_arguments()
        
        try:
            # Setup logging level
            if args.verbose:
                logger.setLevel("DEBUG")
                logger.debug("Verbose logging enabled")
            
            # Initialize core
            logger.info("Initializing TokIntel core...")
            self.core = TokIntelCore(args.config)
            
            # Apply CLI overrides
            if args.model:
                self.core.update_config({"model": args.model})
                logger.info(f"Model override: {args.model}")
            if args.language:
                self.core.update_config({"language": args.language})
                logger.info(f"Language override: {args.language}")
            
            # Handle UI mode
            if args.ui:
                logger.info("Launching Streamlit UI...")
                self._launch_streamlit()
                return
            
            # Handle CLI processing
            if not args.input:
                logger.error("Input path is required for CLI mode")
                sys.exit(1)
            
            self._process_cli_input(args)
            
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
            sys.exit(1)
        except TokIntelError as e:
            logger.error(f"TokIntel error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)
    
    def _launch_streamlit(self):
        """Launch Streamlit interface"""
        try:
            launcher = StreamlitLauncher()
            launcher.launch()
        except Exception as e:
            logger.error(f"Failed to launch Streamlit: {e}")
            sys.exit(1)
    
    def _process_cli_input(self, args):
        """Process input in CLI mode"""
        logger.info(f"Processing input: {args.input}")
        
        # Process input
        if os.path.isfile(args.input):
            # Single file
            logger.info(f"Processing single file: {args.input}")
            results = asyncio.run(self.core.process_video(args.input))
            results = [results] if results else []
        else:
            # Directory
            logger.info(f"Processing directory: {args.input}")
            results = self.core.run_sync(args.input)
        
        # Summary
        logger.info(f"Processing completed. {len(results)} videos analyzed.")
        
        if results:
            logger.info(f"Results saved to: {args.output}")
            
            # Display summary
            self._display_summary(results)
    
    def _display_summary(self, results: List[Dict[str, Any]]):
        """Display processing summary"""
        if not results:
            return
        
        logger.info("=== PROCESSING SUMMARY ===")
        
        total_score = 0
        processed_count = 0
        
        for i, result in enumerate(results, 1):
            if "score" in result and "summary" in result:
                score = result["score"].get("score", 0)
                total_score += score
                processed_count += 1
                
                logger.info(f"Video {i}: Score {score:.2f}")
        
        if processed_count > 0:
            avg_score = total_score / processed_count
            logger.info(f"Average score: {avg_score:.2f}")
        
        logger.info("==========================")

def main():
    """Main entry point"""
    logger.info("TokIntel v2 starting...")
    cli = TokIntelCLI()
    cli.run()

if __name__ == "__main__":
    main() 