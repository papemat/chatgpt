#!/usr/bin/env python3
"""
TokIntel v2.1 - Final Release Preparation
Script per preparare il rilascio enterprise finale
"""

from typing import Dict, List, Any, Optional
import os
import sys
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path


class ReleasePreparator:
    """Preparatore per il rilascio finale"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.release_dir = self.project_root / "release" / "TokIntel_v2.1"
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "version": "2.1.0",
            "status": "preparing",
            "steps_completed": [],
            "errors": [],
            "warnings": []
        }
    
    def run_all_preparations(self):
        """Esegue tutte le preparazioni per il rilascio"""
        logger.info("[INFO] Iniziando preparazione rilascio TokIntel v2.1...")
        
        try:
            # Step 1: Pulizia repository
            self.cleanup_repository()
            
            # Step 2: Applicazione fix docstring
            self.apply_docstring_fixes()
            
            # Step 3: Esecuzione test suite
            self.run_test_suite()
            
            # Step 4: Validazione finale
            self.final_validation()
            
            # Step 5: Creazione struttura release
            self.create_release_structure()
            
            # Step 6: Generazione report finale
            self.generate_final_report()
            
            logger.info("[OK] Preparazione rilascio completata con successo!")
            
        except Exception as e:
            self.report["errors"].append(str(e))
            logger.info(f"[ERROR] Errore durante la preparazione: {e}")
            return False
        
        return True
    
    def cleanup_repository(self):
        """Pulisce il repository da file temporanei"""
        logger.info("[INFO] Pulizia repository...")
        
        # File e cartelle da rimuovere
        cleanup_items = [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            "dist",
            "build",
            "*.egg-info"
        ]
        
        for item in cleanup_items:
            if "*" in item:
                # Pattern glob
                for file_path in self.project_root.rglob(item):
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path, ignore_errors=True)
            else:
                # Nome specifico
                item_path = self.project_root / item
                if item_path.exists():
                    if item_path.is_file():
                        item_path.unlink()
                    elif item_path.is_dir():
                        shutil.rmtree(item_path, ignore_errors=True)
        
        self.report["steps_completed"].append("repository_cleanup")
        logger.info("[OK] Repository pulito")
    
    def apply_docstring_fixes(self):
        """Applica i fix per le docstring issues"""
        logger.info("[INFO] Applicazione fix docstring...")
        
        try:
            # Esegui il fixer automatico
            fixer_script = self.project_root / "tools" / "debug_tools" / "docstring_fixes.py"
            
            if fixer_script.exists():
                result = subprocess.run([
                    sys.executable, str(fixer_script), str(self.project_root)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("[OK] Fix docstring applicati")
                    self.report["steps_completed"].append("docstring_fixes")
                else:
                    logger.info(f"[WARN] Warning durante fix docstring: {result.stderr}")
                    self.report["warnings"].append(f"docstring_fixes: {result.stderr}")
            else:
                logger.info("[WARN] Script docstring_fixes.py non trovato")
                self.report["warnings"].append("docstring_fixes_script_not_found")
                
        except Exception as e:
            logger.info(f"[WARN] Errore durante fix docstring: {e}")
            self.report["warnings"].append(f"docstring_fixes_error: {e}")
    
    def run_test_suite(self):
        """Esegue la test suite completa"""
        logger.info("[INFO] Esecuzione test suite...")
        
        try:
            # Esegui pytest
            result = subprocess.run([
                sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                logger.info("[OK] Test suite completata con successo")
                self.report["steps_completed"].append("test_suite")
                
                # Estrai statistiche test
                test_output = result.stdout
                if "passed" in test_output:
                    passed_tests = [line for line in test_output.split('\n') if "passed" in line]
                    self.report["test_stats"] = passed_tests[-1] if passed_tests else "Unknown"
            else:
                logger.info(f"[WARN] Test suite con warning: {result.stderr}")
                self.report["warnings"].append(f"test_suite: {result.stderr}")
                
        except Exception as e:
            logger.info(f"[WARN] Errore durante test suite: {e}")
            self.report["warnings"].append(f"test_suite_error: {e}")
    
    def final_validation(self):
        """Validazione finale del progetto"""
        logger.info("[INFO] Validazione finale...")
        
        try:
            # Esegui post-audit validator
            validator_script = self.project_root / "tools" / "debug_tools" / "post_audit_validator.py"
            
            if validator_script.exists():
                result = subprocess.run([
                    sys.executable, str(validator_script)
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0:
                    logger.info("[OK] Validazione finale completata")
                    self.report["steps_completed"].append("final_validation")
                else:
                    logger.info(f"[WARN] Warning durante validazione: {result.stderr}")
                    self.report["warnings"].append(f"final_validation: {result.stderr}")
            else:
                logger.info("[WARN] Post-audit validator non trovato")
                self.report["warnings"].append("post_audit_validator_not_found")
                
        except Exception as e:
            logger.info(f"[WARN] Errore durante validazione: {e}")
            self.report["warnings"].append(f"final_validation_error: {e}")
    
    def create_release_structure(self):
        """Crea la struttura finale di release"""
        logger.info("[INFO] Creazione struttura release...")
        
        try:
            # Crea directory release se non esiste
            self.release_dir.mkdir(parents=True, exist_ok=True)
            
            # File e cartelle da copiare
            items_to_copy = [
                "core/",
                "agent/",
                "llm/",
                "ui/",
                "tools/",
                "tests/",
                "config/",
                "logs/",
                "README.md",
                "VERSION.txt",
                "requirements.txt",
                "requirements_dev.txt",
                "config.yaml.example",
                "run.sh",
                "install.sh",
                ".github/",
                ".gitignore"
            ]
            
            for item in items_to_copy:
                source = self.project_root / item
                destination = self.release_dir / item
                
                if source.exists():
                    if source.is_dir():
                        if destination.exists():
                            shutil.rmtree(destination)
                        shutil.copytree(source, destination)
                    else:
                        shutil.copy2(source, destination)
            
            # Crea file di checksum
            self.create_checksum_file()
            
            self.report["steps_completed"].append("release_structure")
            logger.info("[OK] Struttura release creata")
            
        except Exception as e:
            logger.info(f"[ERROR] Errore durante creazione struttura release: {e}")
            self.report["errors"].append(f"release_structure: {e}")
    
    def create_checksum_file(self):
        """Crea file di checksum per i file principali"""
        import hashlib
        
        checksums = {}
        
        # File importanti da verificare
        important_files = [
            "main.py",
            "core/config.py",
            "core/logger.py",
            "agent/synthesis.py",
            "llm/handler.py",
            "ui/interface.py"
        ]
        
        for file_name in important_files:
            file_path = self.release_dir / file_name
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    content = f.read()
                    checksum = hashlib.sha256(content).hexdigest()
                    checksums[file_name] = checksum
        
        # Salva checksums
        checksum_file = self.release_dir / "checksums.json"
        with open(checksum_file, 'w') as f:
            json.dump(checksums, f, indent=2)
        
        self.report["checksums"] = checksums
    
    def generate_final_report(self):
        """Genera il report finale del rilascio"""
        logger.info("[REPORT] Generazione report finale...")
        
        # Aggiorna status
        if self.report["errors"]:
            self.report["status"] = "failed"
        elif self.report["warnings"]:
            self.report["status"] = "completed_with_warnings"
        else:
            self.report["status"] = "completed_successfully"
        
        # Salva report
        report_file = self.release_dir / "release_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        # Crea report markdown
        self.create_markdown_report()
        
        logger.info("[OK] Report finale generato")
    
    def create_markdown_report(self):
        """Crea report markdown leggibile"""
        report_md = f"""# TokIntel v2.1 - Release Report

**Data**: {self.report['timestamp']}  
**Versione**: {self.report['version']}  
**Status**: {self.report['status']}

## [OK] Step Completati

"""
        
        for step in self.report["steps_completed"]:
            report_md += f"- [OK] {step}\n"
        
        if self.report["warnings"]:
            report_md += "\n## [WARN] Warning\n\n"
            for warning in self.report["warnings"]:
                report_md += f"- [WARN] {warning}\n"
        
        if self.report["errors"]:
            report_md += "\n## [ERROR] Errori\n\n"
            for error in self.report["errors"]:
                report_md += f"- [ERROR] {error}\n"
        
        if "test_stats" in self.report:
            report_md += f"\n## [INFO] Test Statistics\n\n{self.report['test_stats']}\n"
        
        if "checksums" in self.report:
            report_md += "\n## [INFO] Checksums\n\n"
            for file_name, checksum in self.report["checksums"].items():
                report_md += f"- `{file_name}`: `{checksum[:16]}...`\n"
        
        report_md += f"""

## [INFO] Prossimi Step

1. **Verifica locale**: Testa l'installazione con `./install.sh`
2. **Test funzionale**: Verifica che l'interfaccia funzioni con `./run.sh`
3. **GitHub**: Push su repository e verifica CI/CD
4. **Documentazione**: Aggiorna README con istruzioni finali

---
*Generato automaticamente da TokIntel v2.1 Release Preparator*
"""
        
        report_file = self.release_dir / "RELEASE_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_md)


def main():
    """Main function"""
    if len(sys.argv) != 2:
        logger.info("Usage: python final_release_prep.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    preparator = ReleasePreparator(project_root)
    
    success = preparator.run_all_preparations()
    
    if success:
        logger.info("\n[OK] Rilascio TokIntel v2.1 pronto!")
        logger.info(f"f"[INFO] Controlla la cartella: {preparator.release_dir}"")
        logger.info("[REPORT] Report disponibile in: release/TokIntel_v2.1/release_report.json")
    else:
        logger.info("\n[ERROR] Preparazione rilascio fallita")
        sys.exit(1)


if __name__ == "__main__":
    main() 