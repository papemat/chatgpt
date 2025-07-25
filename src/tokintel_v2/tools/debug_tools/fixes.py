#!/usr/bin/env python3
"""
TokIntel v2 - Specific Fixes
Correzioni specifiche per i problemi identificati nel codice
"""

import re
import os
import logging
from typing import List, Dict, Any

# Setup logging
logger = logging.getLogger(__name__)

class TokIntelFixes:
    """Specific fixes for TokIntel v2 issues"""
    
    @staticmethod
    def fix_asyncio_deprecations(file_path: str) -> List[str]:
        """Fix deprecated asyncio.get_event_loop() calls"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix asyncio.get_event_loop().time()
        old_pattern = r'asyncio\.get_event_loop\(\)\.time\(\)'
        new_pattern = 'asyncio.get_event_loop().time()'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, 'asyncio.get_event_loop().time()', content)
            fixes.append("Fixed deprecated asyncio.get_event_loop().time()")
        
        # Fix asyncio.get_event_loop() for run_in_executor
        old_pattern = r'loop = asyncio\.get_event_loop\(\)'
        new_pattern = 'loop = asyncio.get_running_loop()'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_pattern, content)
            fixes.append("Fixed deprecated asyncio.get_event_loop()")
        
        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes
    
    @staticmethod
    def fix_bare_excepts(file_path: str) -> List[str]:
        """Fix bare except clauses"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix bare except clauses
        old_pattern = r'except\s*:'
        new_pattern = 'except Exception:'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_pattern, content)
            fixes.append("Fixed bare except clause")
        
        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes
    
    @staticmethod
    def fix_print_statements(file_path: str) -> List[str]:
        """Replace print statements with logger calls"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add logger import if not present
        if 'logger.info(' in content and 'import logging' not in content:
            # Find the first import line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    lines.insert(i, 'import logging')
                    lines.insert(i + 1, 'logger = logging.getLogger(__name__)')
                    break
            
            content = '\n'.join(lines)
            fixes.append("Added logging import")
        
        # Replace print statements with logger calls
        old_pattern = r'print\s*\(([^)]+)\)'
        
        def replace_logger.info(f"match"):
            args = match.group(1)
            # Handle different print argument types
            if args.strip().startswith('"') or args.strip().startswith("'"):
                return f'logger.info({args})'
            else:
                return f'logger.info(f"{args}")'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, replace_print, content)
            fixes.append("Replaced print statements with logger calls")
        
        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes
    
    @staticmethod
    def fix_imports(file_path: str) -> List[str]:
        """Fix import issues"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove unused imports (basic check)
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                new_lines.append(line)
                continue
            
            # Check for import statements
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Basic check for unused imports
                import_name = line.strip().split()[1].split('.')[0]
                if import_name not in content.replace(line, ''):
                    continue  # Skip this import
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        if len(new_lines) < len(lines):
            content = '\n'.join(new_lines)
            fixes.append("Removed unused imports")
        
        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes
    
    @staticmethod
    def fix_type_hints(file_path: str) -> List[str]:
        """Add missing type hints"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add typing import if not present
        if 'from typing import' not in content and 'import typing' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    lines.insert(i, 'from typing import Dict, List, Any, Optional')
                    break
            
            content = '\n'.join(lines)
            fixes.append("Added typing imports")
        
        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return fixes
    
    @staticmethod
    def apply_all_fixes(file_path: str) -> Dict[str, List[str]]:
        """Apply all fixes to a file"""
        all_fixes = {}
        
        # Apply each fix
        fixes = TokIntelFixes.fix_asyncio_deprecations(file_path)
        if fixes:
            all_fixes['asyncio'] = fixes
        
        fixes = TokIntelFixes.fix_bare_excepts(file_path)
        if fixes:
            all_fixes['exceptions'] = fixes
        
        fixes = TokIntelFixes.fix_print_statements(file_path)
        if fixes:
            all_fixes['logging'] = fixes
        
        fixes = TokIntelFixes.fix_imports(file_path)
        if fixes:
            all_fixes['imports'] = fixes
        
        fixes = TokIntelFixes.fix_type_hints(file_path)
        if fixes:
            all_fixes['typing'] = fixes
        
        return all_fixes

def main():
    """Apply fixes to all Python files"""
    project_root = Path(".")
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    logger.info(f"Applying fixes to {len(python_files)} Python files...")
    
    total_fixes = {}
    
    for py_file in python_files:
        logger.info(f"Processing {py_file}...")
        fixes = TokIntelFixes.apply_all_fixes(str(py_file))
        
        if fixes:
            total_fixes[str(py_file)] = fixes
            logger.info(f"  Applied fixes: {list(fixes.keys())}")
    
    logger.info(f"\nApplied fixes to {len(total_fixes)} files")
    
    # Save fix report
    import json
    with open('fixes_report.json', 'w') as f:
        json.dump(total_fixes, f, indent=2)
    
    logger.info("Fix report saved to fixes_report.json")

if __name__ == "__main__":
    import os
    main() 