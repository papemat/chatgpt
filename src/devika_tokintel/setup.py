#!/usr/bin/env python3
"""
Setup script for Devika TokIntel - Enhanced AI Integration System
Automated setup and configuration for local LLM management
"""
import os
import sys
import subprocess
import platform
import json
import yaml
from pathlib import Path
from datetime import datetime

class DevikaSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tokintel_path = self.project_root.parent / "TokIntel_v2"
        self.log_file = self.project_root / "logs" / "setup.log"
        
        # Create logs directory
        self.log_file.parent.mkdir(exist_ok=True)
        
        print("[INFO] Devika TokIntel - Enhanced AI Integration System")
        print("=" * 60)
        print(f"[INFO] Project Root: {self.project_root}")
        print(f"🤖 TokIntel Path: {self.tokintel_path}")
        print()
    
    def log(self, message: str):
        """Log message to file and print to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.log("[INFO] Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log("[ERROR] Python 3.8+ required. Current version: {}.{}".format(version.major, version.minor))
            return False
        
        self.log(f"[OK] Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    
    def check_system_info(self):
        """Display system information"""
        self.log("💻 System Information:")
        self.log(f"   OS: {platform.system()} {platform.release()}")
        self.log(f"   Architecture: {platform.machine()}")
        self.log(f"   Python: {platform.python_version()}")
        self.log(f"   Working Directory: {os.getcwd()}")
    
    def check_tokintel_structure(self):
        """Check if TokIntel_v2 structure is correct"""
        self.log("[INFO] Checking TokIntel_v2 structure...")
        
        if not self.tokintel_path.exists():
            self.log("[ERROR] TokIntel_v2 directory not found!")
            self.log(f"   Expected: {self.tokintel_path}")
            self.log("   Please ensure TokIntel_v2 is in the parent directory")
            return False
        
        required_dirs = [
            "llm",
            "utils", 
            "audio",
            "huggingface"
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.tokintel_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            self.log(f"[ERROR] Missing directories in TokIntel_v2: {', '.join(missing_dirs)}")
            return False
        
        self.log("[OK] TokIntel_v2 structure verified")
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.log("[INFO] Installing Python dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.log("[ERROR] requirements.txt not found!")
            return False
        
        try:
            # Read requirements
            with open(requirements_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            self.log(f"[INFO] Found {len(requirements)} dependencies to install")
            
            # Install each dependency
            for req in requirements:
                self.log(f"   Installing: {req}")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", req], 
                                 check=True, capture_output=True, text=True)
                    self.log(f"   [OK] {req} installed successfully")
                except subprocess.CalledProcessError as e:
                    self.log(f"   [WARN]️  Failed to install {req}: {e}")
            
            self.log("[OK] Dependencies installation completed")
            return True
            
        except Exception as e:
            self.log(f"[ERROR] Error installing dependencies: {e}")
            return False
    
    def check_llm_backends(self):
        """Check availability of LLM backends"""
        self.log("🤖 Checking LLM backends availability...")
        
        backends_status = {
            "lmstudio": False,
            "ollama": False
        }
        
        # Check LM Studio
        try:
            import requests
            response = requests.get("http://localhost:1234/v1/models", timeout=5)
            if response.status_code == 200:
                backends_status["lmstudio"] = True
                self.log("[OK] LM Studio server is running")
            else:
                self.log("[WARN]️  LM Studio server not responding")
        except:
            self.log("[WARN]️  LM Studio server not accessible")
        
        # Check Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                backends_status["ollama"] = True
                self.log("[OK] Ollama server is running")
            else:
                self.log("[WARN]️  Ollama server not responding")
        except:
            self.log("[WARN]️  Ollama server not accessible")
        
        # Summary
        available_backends = [k for k, v in backends_status.items() if v]
        if available_backends:
            self.log(f"[OK] Available backends: {', '.join(available_backends)}")
        else:
            self.log("[WARN]️  No LLM backends currently available")
            self.log("   You can start them manually or use the test tasks to get instructions")
        
        return backends_status
    
    def create_config_files(self):
        """Create default configuration files if they don't exist"""
        self.log("⚙️  Setting up configuration files...")
        
        # Create devika_config.yaml if it doesn't exist
        devika_config = self.project_root / "devika_config.yaml"
        if not devika_config.exists():
            self.log("[INFO] Creating devika_config.yaml...")
            
            default_config = {
                "project_name": "Devika TokIntel",
                "version": "2.0.0",
                "description": "Enhanced AI Integration System with Automatic Model Management",
                "tokintel_path": str(self.tokintel_path),
                "logs_dir": "logs",
                "exports_dir": "exports",
                "reports_dir": "reports",
                "backups_dir": "backups",
                "default_tasks": [
                    "test_config",
                    "system_health",
                    "test_model_management"
                ],
                "llm": {
                    "preferred_backend": "lmstudio",
                    "fallback_strategy": "auto",
                    "lmstudio": {
                        "base_url": "http://localhost:1234/v1/chat/completions",
                        "model": "mistral",
                        "timeout": 30,
                        "max_retries": 3
                    },
                    "ollama": {
                        "base_url": "http://localhost:11434",
                        "model": "mistral",
                        "timeout": 30,
                        "max_retries": 3
                    }
                }
            }
            
            with open(devika_config, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            
            self.log("[OK] devika_config.yaml created")
        
        # Create project_map.yaml if it doesn't exist
        project_map = self.project_root / "project_map.yaml"
        if not project_map.exists():
            self.log("[INFO] Creating project_map.yaml...")
            
            default_map = {
                "project_name": "TokIntel_v2",
                "version": "2.0.0",
                "description": "AI Integration Framework",
                "modules": {
                    "config": "core/config.py",
                    "prompts": "llm/prompts.py",
                    "handler": "llm/handler.py",
                    "ui": "ui/interface.py",
                    "agents": "agents/",
                    "llm_clients": {
                        "lmstudio": "llm/lmstudio_client.py",
                        "ollama": "llm/ollama_client.py"
                    },
                    "utils": {
                        "router": "utils/llm_router.py"
                    },
                    "integrations": {
                        "whisper": "audio/whisper_transcriber.py",
                        "huggingface": "huggingface/inference.py"
                    }
                },
                "tasks": {
                    "test": "tasks/test_*.py",
                    "benchmark": "tasks/benchmark_*.py",
                    "maintenance": "tasks/*_maintenance.py"
                }
            }
            
            with open(project_map, 'w', encoding='utf-8') as f:
                yaml.dump(default_map, f, default_flow_style=False, allow_unicode=True)
            
            self.log("[OK] project_map.yaml created")
    
    def create_directories(self):
        """Create necessary directories"""
        self.log("[INFO] Creating necessary directories...")
        
        directories = [
            "logs",
            "exports", 
            "reports",
            "backups",
            "temp"
        ]
        
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)
            self.log(f"   [OK] Created: {dir_name}/")
    
    def run_initial_tests(self):
        """Run initial system tests"""
        self.log("[INFO] Running initial system tests...")
        
        try:
            # Test imports
            sys.path.insert(0, str(self.tokintel_path))
            
            # Test basic imports
            test_imports = [
                ("utils.llm_router", "LLM Router"),
                ("llm.lmstudio_client", "LM Studio Client"),
                ("llm.ollama_client", "Ollama Client")
            ]
            
            for module, name in test_imports:
                try:
                    __import__(module)
                    self.log(f"   [OK] {name} import successful")
                except ImportError as e:
                    self.log(f"   [WARN]️  {name} import failed: {e}")
            
            # Test task runner
            try:
                from tasks.task_runner import tasks
                self.log(f"   [OK] Task runner loaded with {len(tasks)} tasks")
            except Exception as e:
                self.log(f"   [WARN]️  Task runner test failed: {e}")
            
        except Exception as e:
            self.log(f"[ERROR] Initial tests failed: {e}")
            return False
        
        self.log("[OK] Initial tests completed")
        return True
    
    def generate_setup_report(self):
        """Generate setup completion report"""
        self.log("[REPORT] Generating setup report...")
        
        report = {
            "setup_timestamp": datetime.now().isoformat(),
            "system_info": {
                "os": platform.system(),
                "version": platform.release(),
                "architecture": platform.machine(),
                "python_version": platform.python_version()
            },
            "project_paths": {
                "devika_root": str(self.project_root),
                "tokintel_path": str(self.tokintel_path)
            },
            "setup_status": "completed",
            "next_steps": [
                "Run 'python devika.py test_model_management' to check model status",
                "Run 'python devika.py system_health' for full system check",
                "Run 'python devika.py benchmark_llm' to test LLM performance",
                "Use 'launch.bat' for quick startup on Windows"
            ]
        }
        
        report_file = self.project_root / "logs" / "setup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log("[OK] Setup report generated")
        return report
    
    def run(self):
        """Run complete setup process"""
        self.log("[INFO] Starting Devika TokIntel setup...")
        
        # Step 1: System checks
        if not self.check_python_version():
            return False
        
        self.check_system_info()
        
        # Step 2: Structure verification
        if not self.check_tokintel_structure():
            return False
        
        # Step 3: Create directories
        self.create_directories()
        
        # Step 4: Install dependencies
        if not self.install_dependencies():
            self.log("[WARN]️  Some dependencies may not have installed correctly")
        
        # Step 5: Create config files
        self.create_config_files()
        
        # Step 6: Check LLM backends
        backends_status = self.check_llm_backends()
        
        # Step 7: Run initial tests
        self.run_initial_tests()
        
        # Step 8: Generate report
        report = self.generate_setup_report()
        
        # Final summary
        self.log("")
        self.log("[INFO] Setup completed successfully!")
        self.log("=" * 60)
        self.log("[INFO] Next Steps:")
        for step in report["next_steps"]:
            self.log(f"   • {step}")
        self.log("")
        self.log("💡 Quick Start:")
        self.log("   python devika.py test_model_management")
        self.log("   python devika.py system_health")
        self.log("")
        self.log("[INFO] Logs and reports saved in 'logs/' directory")
        
        return True

def main():
    """Main setup function"""
    setup = DevikaSetup()
    success = setup.run()
    
    if success:
        print("\n[OK] Setup completed successfully!")
        print("[INFO] You can now use Devika TokIntel with automatic model management!")
    else:
        print("\n[ERROR] Setup encountered issues. Check logs for details.")
        print("💡 You can still try running individual tasks manually.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 