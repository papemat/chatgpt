"""
Streamlit Launcher Module
Handles launching the Streamlit interface
"""

from typing import Dict, List, Any, Optional
import logging
logger = logging.getLogger(__name__)
import subprocess
import sys

# Try to import streamlit
try:
    import streamlit
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    streamlit = None

logger = setup_logger(__name__)

class StreamlitLauncher:
    """Handles launching Streamlit interface"""
    
    def __init__(self):
        """Initialize Streamlit launcher"""
        self.streamlit_path = Path(__file__).parent / "interface.py"
    
    def launch(self):
        """Launch Streamlit interface"""
        try:
            if not STREAMLIT_AVAILABLE:
                logger.error("Streamlit not installed. Install with: pip install streamlit")
                sys.exit(1)
            
            logger.info("Launching Streamlit interface...")
            
            if not self.streamlit_path.exists():
                logger.error("Streamlit interface not found. Please ensure ui/interface.py exists.")
                sys.exit(1)
            
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", str(self.streamlit_path)
            ])
            
        except Exception as e:
            logger.error(f"Failed to launch Streamlit: {e}")
            sys.exit(1) 