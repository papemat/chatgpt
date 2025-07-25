#!/usr/bin/env python3
"""
TokIntel v2 - Debug & Audit Script
Script automatico per audit, debug e rimozione warning del codice
"""

from typing import Dict, List, Any, Optional
import os
import sys
import subprocess
import asyncio
import logging
import json
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TokIntelAuditor:
    """Auditor per TokIntel v2 - identifica e risolve warning e problemi"""
    
    def __init__(self, project_root: str = "."):
        """Initialize auditor"""
        self.project_root = Path(project_root)
        self.report = {
            "timestamp": time.time(),
            "warnings_found": [],
            "errors_found": [],
            "fixes_applied": [],
            "imports_removed": [],
            "style_issues": [],
            "performance_issues": [],
            "security_issues": []
        }
        
        # Python files to audit
        self.python_files = []
        self._discover_python_files()
    
    def _discover_python_files(self):
        """Discover all Python files in the project"""
        for root, dirs, files in os.walk(self.project_root):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
            
            for file in files:
                if file.endswith('.py'):
                    self.python_files.append(Path(root) / file)
        
        logger.info(f"Found {len(self.python_files)} Python files to audit")
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete audit of the codebase"""
        logger.info("Starting TokIntel v2 audit...")
        
        try:
            # 1. Check for unused imports
            self._check_unused_imports()
            
            # 2. Run style checks
            self._run_style_checks()
            
            # 3. Run type checking
            self._run_type_checks()
            
            # 4. Run linting
            self._run_linting()
            
            # 5. Check for common issues
            self._check_common_issues()
            
            # 6. Check for async/await issues
            self._check_async_issues()
            
            # 7. Check for security issues
            self._check_security_issues()
            
            # 8. Generate report
            self._generate_report()
            
            logger.info("Audit completed successfully")
            return self.report
            
        except Exception as e:
            logger.error(f"Audit failed: {e}")
            self.report["errors_found"].append(f"Audit failed: {e}")
            return self.report
    
    def _check_unused_imports(self):
        """Check for unused imports using autoflake"""
        logger.info("Checking for unused imports...")
        
        try:
            for py_file in self.python_files:
                result = subprocess.run(
                    ['autoflake', '--remove-all-unused-imports', '--in-place', str(py_file)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.report["fixes_applied"].append(f"Removed unused imports from {py_file}")
                elif result.stderr:
                    self.report["warnings_found"].append(f"Import check warning in {py_file}: {result.stderr}")
                    
        except FileNotFoundError:
            logger.warning("autoflake not found, skipping unused import check")
            self.report["warnings_found"].append("autoflake not available for import cleanup")
    
    def _run_style_checks(self):
        """Run Black formatter and style checks"""
        logger.info("Running style checks...")
        
        try:
            # Run Black formatter
            result = subprocess.run(
                ['black', '--check', '--diff', str(self.project_root)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.report["style_issues"].append("Code formatting issues found")
                logger.info("Applying Black formatting...")
                
                # Apply Black formatting
                subprocess.run(['black', str(self.project_root)], check=True)
                self.report["fixes_applied"].append("Applied Black formatting")
                
        except FileNotFoundError:
            logger.warning("Black not found, skipping style checks")
            self.report["warnings_found"].append("Black not available for style formatting")
    
    def _run_type_checks(self):
        """Run MyPy type checking"""
        logger.info("Running type checks...")
        
        try:
            result = subprocess.run(
                ['mypy', str(self.project_root)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.report["warnings_found"].append(f"Type checking issues: {result.stdout}")
                
        except FileNotFoundError:
            logger.warning("MyPy not found, skipping type checks")
            self.report["warnings_found"].append("MyPy not available for type checking")
    
    def _run_linting(self):
        """Run Flake8 linting"""
        logger.info("Running linting checks...")
        
        try:
            result = subprocess.run(
                ['flake8', str(self.project_root)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.report["style_issues"].append(f"Linting issues: {result.stdout}")
                
        except FileNotFoundError:
            logger.warning("Flake8 not found, skipping linting")
            self.report["warnings_found"].append("Flake8 not available for linting")
    
    def _check_common_issues(self):
        """Check for common Python issues"""
        logger.info("Checking for common issues...")
        
        common_patterns = [
            (r'import\s+\*', "Wildcard imports detected"),
            (r'except\s*:', "Bare except clauses detected"),
            (r'print\s*\(', "Print statements detected (use logger instead)"),
            (r'input\s*\(', "Input statements detected (security concern)"),
            (r'eval\s*\(', "Eval statements detected (security concern)"),
            (r'exec\s*\(', "Exec statements detected (security concern)"),
        ]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, message in common_patterns:
                    import re
                    if re.search(pattern, content):
                        self.report["warnings_found"].append(f"{message} in {py_file}")
                        
            except Exception as e:
                self.report["errors_found"].append(f"Error reading {py_file}: {e}")
    
    def _check_async_issues(self):
        """Check for async/await issues"""
        logger.info("Checking for async/await issues...")
        
        async_patterns = [
            (r'async def.*\n.*await', "Async function with await"),
            (r'await.*\n.*async def', "Await outside async function"),
            (r'asyncio\.run.*asyncio\.run', "Nested asyncio.run calls"),
        ]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, message in async_patterns:
                    import re
                    if re.search(pattern, content):
                        self.report["warnings_found"].append(f"{message} in {py_file}")
                        
            except Exception as e:
                self.report["errors_found"].append(f"Error reading {py_file}: {e}")
    
    def _check_security_issues(self):
        """Check for security issues"""
        logger.info("Checking for security issues...")
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']*["\']', "Hardcoded password detected"),
            (r'api_key\s*=\s*["\'][^"\']*["\']', "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'][^"\']*["\']', "Hardcoded secret detected"),
            (r'\.env', "Environment file reference"),
        ]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, message in security_patterns:
                    import re
                    if re.search(pattern, content):
                        self.report["security_issues"].append(f"{message} in {py_file}")
                        
            except Exception as e:
                self.report["errors_found"].append(f"Error reading {py_file}: {e}")
    
    def _generate_report(self):
        """Generate audit report"""
        logger.info("Generating audit report...")
        
        report_path = self.project_root / "audit_report.json"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, indent=2, default=str)
            
            logger.info(f"Audit report saved to: {report_path}")
            
        except Exception as e:
            logger.error(f"Failed to save audit report: {e}")
    
    def print_summary(self):
        """Print audit summary"""
        logger.info("\n" + "="*50)
        logger.info("TOKINTEL V2 AUDIT SUMMARY")
        logger.info("="*50)
        
        logger.info(f"Python files audited: {len(self.python_files)}")
        logger.info(f"Warnings found: {len(self.report['warnings_found'])}")
        logger.info(f"Errors found: {len(self.report['errors_found'])}")
        logger.info(f"Fixes applied: {len(self.report['fixes_applied'])}")
        logger.info(f"Style issues: {len(self.report['style_issues'])}")
        logger.info(f"Security issues: {len(self.report['security_issues'])}")
        
        if self.report['warnings_found']:
            logger.info("\nWARNINGS:")
            for warning in self.report['warnings_found'][:5]:  # Show first 5
                logger.info(f"  - {warning}")
        
        if self.report['errors_found']:
            logger.info("\nERRORS:")
            for error in self.report['errors_found'][:5]:  # Show first 5
                logger.info(f"  - {error}")
        
        if self.report['fixes_applied']:
            logger.info("\nFIXES APPLIED:")
            for fix in self.report['fixes_applied'][:5]:  # Show first 5
                logger.info(f"  - {fix}")
        
        logger.info("\n" + "="*50)

def main():
    """Main function"""
    logger.info("TokIntel v2 - Debug & Audit Tool")
    logger.info("="*40)
    
    # Run audit
    auditor = TokIntelAuditor()
    report = auditor.run_full_audit()
    
    # Print summary
    auditor.print_summary()
    
    # Return exit code based on issues found
    if report['errors_found']:
        sys.exit(1)
    elif report['warnings_found']:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 