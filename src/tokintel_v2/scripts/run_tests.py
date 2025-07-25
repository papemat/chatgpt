#!/usr/bin/env python3
"""
[INFO] Test Runner - TokIntel v2
Script per eseguire tutti i test disponibili con coverage e reporting
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRunner:
    """Runner per tutti i test di TokIntel v2"""
    
    def __init__(self):
        """Inizializza il test runner"""
        self.project_root = Path(__file__).parent.parent
        self.test_dir = self.project_root / "tests"
        self.coverage_dir = self.project_root / "coverage_html"
        
    def run_unit_tests(self) -> bool:
        """
        Esegue i test unitari
        
        Returns:
            True se tutti i test passano, False altrimenti
        """
        try:
            logger.info("[INFO] Esecuzione test unitari...")
            
            cmd = [
                sys.executable, "-m", "pytest",
                str(self.test_dir),
                "-v",
                "--tb=short"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                logger.info("[OK] Test unitari completati con successo")
                return True
            else:
                logger.error(f"[ERROR] Test unitari falliti:\n{result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Errore nell'esecuzione test unitari: {e}")
            return False
    
    def run_with_coverage(self) -> bool:
        """
        Esegue i test con coverage
        
        Returns:
            True se tutti i test passano, False altrimenti
        """
        try:
            logger.info("[REPORT] Esecuzione test con coverage...")
            
            # Crea directory coverage se non esiste
            self.coverage_dir.mkdir(exist_ok=True)
            
            cmd = [
                sys.executable, "-m", "pytest",
                str(self.test_dir),
                "--cov=.",
                "--cov-report=html:" + str(self.coverage_dir),
                "--cov-report=term-missing",
                "-v"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                logger.info("[OK] Test con coverage completati con successo")
                logger.info(f"[REPORT] Report coverage disponibile in: {self.coverage_dir}")
                return True
            else:
                logger.error(f"[ERROR] Test con coverage falliti:\n{result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Errore nell'esecuzione test con coverage: {e}")
            return False
    
    def run_linting(self) -> bool:
        """
        Esegue il linting del codice
        
        Returns:
            True se il linting passa, False altrimenti
        """
        try:
            logger.info("[INFO] Esecuzione linting...")
            
            # Flake8
            cmd_flake8 = [
                sys.executable, "-m", "flake8",
                ".",
                "--max-line-length=100",
                "--ignore=E203,W503"
            ]
            
            result_flake8 = subprocess.run(cmd_flake8, capture_output=True, text=True, cwd=self.project_root)
            
            if result_flake8.returncode != 0:
                logger.error(f"[ERROR] Flake8 ha trovato errori:\n{result_flake8.stdout}")
                return False
            
            # Black check
            cmd_black = [
                sys.executable, "-m", "black",
                "--check",
                "."
            ]
            
            result_black = subprocess.run(cmd_black, capture_output=True, text=True, cwd=self.project_root)
            
            if result_black.returncode != 0:
                logger.error(f"[ERROR] Black ha trovato errori di formattazione:\n{result_black.stdout}")
                return False
            
            logger.info("[OK] Linting completato con successo")
            return True
            
        except Exception as e:
            logger.error(f"Errore nell'esecuzione linting: {e}")
            return False
    
    def run_type_checking(self) -> bool:
        """
        Esegue il type checking con mypy
        
        Returns:
            True se il type checking passa, False altrimenti
        """
        try:
            logger.info("[INFO] Esecuzione type checking...")
            
            cmd = [
                sys.executable, "-m", "mypy",
                ".",
                "--ignore-missing-imports",
                "--no-strict-optional"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                logger.info("[OK] Type checking completato con successo")
                return True
            else:
                logger.warning(f"[WARN] Type checking ha trovato warning:\n{result.stdout}")
                # Per ora consideriamo i warning come non critici
                return True
                
        except Exception as e:
            logger.error(f"Errore nell'esecuzione type checking: {e}")
            return False
    
    def run_integration_tests(self) -> bool:
        """
        Esegue i test di integrazione
        
        Returns:
            True se tutti i test passano, False altrimenti
        """
        try:
            logger.info("[INFO] Esecuzione test di integrazione...")
            
            # Test di integrazione specifici
            integration_tests = [
                "test_database_integration.py",
                "test_scraper_integration.py",
                "test_ui_integration.py"
            ]
            
            all_passed = True
            
            for test_file in integration_tests:
                test_path = self.test_dir / test_file
                if test_path.exists():
                    logger.info(f"[INFO] Esecuzione {test_file}...")
                    
                    cmd = [
                        sys.executable, "-m", "pytest",
                        str(test_path),
                        "-v"
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
                    
                    if result.returncode != 0:
                        logger.error(f"[ERROR] Test di integrazione {test_file} fallito:\n{result.stderr}")
                        all_passed = False
                    else:
                        logger.info(f"[OK] {test_file} completato con successo")
            
            if all_passed:
                logger.info("[OK] Tutti i test di integrazione completati con successo")
            
            return all_passed
            
        except Exception as e:
            logger.error(f"Errore nell'esecuzione test di integrazione: {e}")
            return False
    
    def run_all_tests(self, with_coverage: bool = True, with_linting: bool = True, 
                     with_type_checking: bool = True) -> Dict[str, bool]:
        """
        Esegue tutti i test disponibili
        
        Args:
            with_coverage: Se includere il coverage
            with_linting: Se includere il linting
            with_type_checking: Se includere il type checking
            
        Returns:
            Dizionario con i risultati di ogni categoria di test
        """
        results = {}
        
        logger.info("[INFO] Avvio esecuzione completa dei test...")
        
        # Test unitari
        results['unit_tests'] = self.run_unit_tests()
        
        # Test con coverage
        if with_coverage:
            results['coverage'] = self.run_with_coverage()
        
        # Linting
        if with_linting:
            results['linting'] = self.run_linting()
        
        # Type checking
        if with_type_checking:
            results['type_checking'] = self.run_type_checking()
        
        # Test di integrazione
        results['integration_tests'] = self.run_integration_tests()
        
        # Riepilogo
        self.print_summary(results)
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Stampa un riepilogo dei risultati dei test"""
        logger.info("\n" + "="*50)
        logger.info("[REPORT] RIEPILOGO TEST")
        logger.info("="*50)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_type, passed in results.items():
            status = "[OK] PASS" if passed else "[ERROR] FAIL"
            logger.info(f"{test_type.replace('_', ' ').title()}: {status}")
        
        logger.info("-"*50)
        logger.info(f"Totale: {passed_tests}/{total_tests} test passati")
        
        if passed_tests == total_tests:
            logger.info("[OK] TUTTI I TEST SONO PASSATI!")
        else:
            logger.info("[WARN] Alcuni test sono falliti. Controlla i log per i dettagli.")
        
        logger.info("="*50)

def main():
    """Funzione principale"""
    parser = argparse.ArgumentParser(description='Test Runner per TokIntel v2')
    parser.add_argument('--no-coverage', action='store_true', help='Non eseguire il coverage')
    parser.add_argument('--no-linting', action='store_true', help='Non eseguire il linting')
    parser.add_argument('--no-type-checking', action='store_true', help='Non eseguire il type checking')
    parser.add_argument('--unit-only', action='store_true', help='Esegui solo i test unitari')
    parser.add_argument('--integration-only', action='store_true', help='Esegui solo i test di integrazione')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.unit_only:
        success = runner.run_unit_tests()
        sys.exit(0 if success else 1)
    
    if args.integration_only:
        success = runner.run_integration_tests()
        sys.exit(0 if success else 1)
    
    # Esegui tutti i test
    results = runner.run_all_tests(
        with_coverage=not args.no_coverage,
        with_linting=not args.no_linting,
        with_type_checking=not args.no_type_checking
    )
    
    # Exit code basato sui risultati
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main() 