"""
Streamlit Launcher Module
Handles launching the Streamlit interface
"""

from typing import Dict, List, Any, Optional
import logging
import subprocess
import sys
import socket
from pathlib import Path
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

from TokIntel_v2.core.logger import setup_logger

# Try to import streamlit
try:
    import streamlit
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    streamlit = None

logger = setup_logger(__name__)

def is_port_open(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

class StreamlitLauncher:
    """Handles launching Streamlit interface"""
    
    def __init__(self):
        """Initialize Streamlit launcher"""
        self.streamlit_path = Path(__file__).parent / "interface.py"
        self.port = 8502  # Default port for TokIntel v2
    
    def launch(self):
        """Launch Streamlit interface"""
        try:
            if not STREAMLIT_AVAILABLE:
                logger.error("Streamlit not installed. Install with: pip install streamlit")
                sys.exit(1)
            
            # Check if port is already in use
            if is_port_open(self.port):
                logger.error(f"[ERROR] La porta {self.port} è già in uso. Chiudi l'altro processo o cambia porta.")
                sys.exit(1)
            
            logger.info(f"Launching Streamlit interface on port {self.port}...")
            
            if not self.streamlit_path.exists():
                logger.error("Streamlit interface not found. Please ensure ui/interface.py exists.")
                sys.exit(1)
            
            # Set environment variable for port
            os.environ["STREAMLIT_SERVER_PORT"] = str(self.port)
            
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", str(self.streamlit_path)
            ])
            
        except Exception as e:
            logger.error(f"Failed to launch Streamlit: {e}")
            sys.exit(1) 