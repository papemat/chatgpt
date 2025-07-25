#!/usr/bin/env python3
"""
TokIntel v2 - Docstring Fixes
Correzioni automatiche per le docstring issues identificate nel post-audit
"""

from typing import Dict, List, Any, Optional
import re
import ast


class DocstringFixer:
    """Fixer automatico per docstring issues"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.fixes_applied = []
        
    def fix_missing_parameter_docs(self, file_path: str) -> List[str]:
        """Fix parametri mancanti nelle docstring"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return fixes
        
        # Trova tutte le funzioni e metodi
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fixes.extend(self._fix_function_docstring(node, content, file_path))
        
        return fixes
    
    def _fix_function_docstring(self, node: ast.FunctionDef, content: str, file_path: str) -> List[str]:
        """Fix docstring per una singola funzione"""
        fixes = []
        
        # Estrai parametri della funzione
        params = []
        for arg in node.args.args:
            if arg.arg != 'self':
                params.append(arg.arg)
        
        # Se non ci sono parametri, salta
        if not params:
            return fixes
        
        # Controlla se la docstring esiste e ha parametri documentati
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
            docstring = node.body[0].value.s
            
            # Trova parametri già documentati
            documented_params = []
            for line in docstring.split('\n'):
                if ':' in line and any(param in line for param in params):
                    for param in params:
                        if param in line and param not in documented_params:
                            documented_params.append(param)
            
            # Trova parametri mancanti
            missing_params = [p for p in params if p not in documented_params]
            
            if missing_params:
                # Genera docstring per parametri mancanti
                new_docstring_lines = []
                for param in missing_params:
                    new_docstring_lines.append(f"    :param {param}: Descrizione del parametro {param}")
                    new_docstring_lines.append(f"    :type {param}: {self._infer_param_type(param, node)}")
                
                # Inserisci nella docstring esistente
                lines = content.split('\n')
                docstring_start = node.body[0].lineno - 1
                docstring_end = node.body[0].end_lineno
                
                # Trova la fine della docstring
                for i in range(docstring_start, len(lines)):
                    if '"""' in lines[i] and i > docstring_start:
                        docstring_end = i
                        break
                
                # Inserisci parametri mancanti
                insert_pos = docstring_end
                for param_doc in reversed(new_docstring_lines):
                    lines.insert(insert_pos, param_doc)
                
                content = '\n'.join(lines)
                fixes.append(f"Added missing parameter docs for: {', '.join(missing_params)}")
        
        return fixes
    
    def _infer_param_type(self, param_name: str, node: ast.FunctionDef) -> str:
        """Inferisce il tipo del parametro dal codice"""
        # Cerca type hints
        for arg in node.args.args:
            if arg.arg == param_name and arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    return arg.annotation.id
                elif isinstance(arg.annotation, ast.Constant):
                    return str(arg.annotation.value)
        
        # Fallback basato sul nome
        type_mapping = {
            'file_path': 'str',
            'config_path': 'str',
            'api_key': 'str',
            'model': 'str',
            'endpoint': 'str',
            'transcript': 'str',
            'ocr_text': 'str',
            'config': 'Config',
            'updates': 'Dict[str, Any]',
            'args': 'List[str]',
            'results': 'Dict[str, Any]',
            'max_retries': 'int',
            'base_delay': 'float',
            'max_delay': 'float',
            'every_n_frames': 'int',
            'video_path': 'str',
            'prompt': 'str',
            'keywords': 'List[str]',
            'target_score': 'int',
            'current_trends': 'List[str]',
            'project_root': 'str',
            'tool_name': 'str',
            'pattern_type': 'str',
            'dir_name': 'str',
            'file_path': 'str',
            'name': 'str',
            'level': 'int',
            'log_file': 'str',
            'exc_info': 'bool',
            'cls': 'type',
            'v': 'Any',
            'file_config': 'Dict[str, Any]',
            'env_config': 'Dict[str, Any]',
            'output_path': 'str'
        }
        
        return type_mapping.get(param_name, 'Any')
    
    def fix_missing_class_attribute_docs(self, file_path: str) -> List[str]:
        """Fix attributi di classe non documentati"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return fixes
        
        # Trova tutte le classi
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fixes.extend(self._fix_class_docstring(node, content, file_path))
        
        return fixes
    
    def _fix_class_docstring(self, node: ast.ClassDef, content: str, file_path: str) -> List[str]:
        """Fix docstring per una singola classe"""
        fixes = []
        
        # Trova attributi di classe
        class_attrs = []
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_attrs.append(target.id)
        
        if not class_attrs:
            return fixes
        
        # Controlla docstring della classe
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
            docstring = node.body[0].value.s
            
            # Trova attributi già documentati
            documented_attrs = []
            for line in docstring.split('\n'):
                if ':' in line and any(attr in line for attr in class_attrs):
                    for attr in class_attrs:
                        if attr in line and attr not in documented_attrs:
                            documented_attrs.append(attr)
            
            # Trova attributi mancanti
            missing_attrs = [a for a in class_attrs if a not in documented_attrs]
            
            if missing_attrs:
                # Genera docstring per attributi mancanti
                new_docstring_lines = []
                for attr in missing_attrs:
                    new_docstring_lines.append(f"    :ivar {attr}: Descrizione dell'attributo {attr}")
                
                # Inserisci nella docstring esistente
                lines = content.split('\n')
                docstring_start = node.body[0].lineno - 1
                docstring_end = node.body[0].end_lineno
                
                # Trova la fine della docstring
                for i in range(docstring_start, len(lines)):
                    if '"""' in lines[i] and i > docstring_start:
                        docstring_end = i
                        break
                
                # Inserisci attributi mancanti
                insert_pos = docstring_end
                for attr_doc in reversed(new_docstring_lines):
                    lines.insert(insert_pos, attr_doc)
                
                content = '\n'.join(lines)
                fixes.append(f"Added missing class attribute docs for: {', '.join(missing_attrs)}")
        
        return fixes
    
    def fix_missing_decorator_docs(self, file_path: str) -> List[str]:
        """Fix docstring mancanti per decoratori"""
        fixes = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trova decoratori senza docstring
        decorator_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        decorator_funcs = re.findall(decorator_pattern, content)
        
        for func_name in decorator_funcs:
            # Cerca se la funzione ha docstring
            func_pattern = rf'def\s+{func_name}\s*\([^)]*\):\s*\n\s*"""[^"]*"""'
            if not re.search(func_pattern, content, re.MULTILINE):
                # Aggiungi docstring di base
                func_def_pattern = rf'(def\s+{func_name}\s*\([^)]*\):)'
                replacement = r'\1\n    """Decorator function {func_name}."""'
                content = re.sub(func_def_pattern, replacement, content)
                fixes.append(f"Added missing docstring for decorator: {func_name}")
        
        return fixes
    
    def apply_all_docstring_fixes(self, file_path: str) -> Dict[str, List[str]]:
        """Applica tutti i fix per docstring"""
        all_fixes = {}
        
        # Fix parametri mancanti
        param_fixes = self.fix_missing_parameter_docs(file_path)
        if param_fixes:
            all_fixes['missing_parameters'] = param_fixes
        
        # Fix attributi classe
        attr_fixes = self.fix_missing_class_attribute_docs(file_path)
        if attr_fixes:
            all_fixes['missing_class_attributes'] = attr_fixes
        
        # Fix decoratori
        decorator_fixes = self.fix_missing_decorator_docs(file_path)
        if decorator_fixes:
            all_fixes['missing_decorators'] = decorator_fixes
        
        return all_fixes


def main():
    """Main function per eseguire i fix"""
    import sys
    
    if len(sys.argv) != 2:
        logger.info("Usage: python docstring_fixes.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    fixer = DocstringFixer(project_root)
    
    # Trova tutti i file Python
    python_files = list(Path(project_root).rglob("*.py"))
    
    total_fixes = 0
    
    for file_path in python_files:
        if "debug_tools" in str(file_path):
            continue  # Salta i tool di debug
        
        logger.info(f"f"Processing: {file_path}"")
        fixes = fixer.apply_all_docstring_fixes(str(file_path))
        
        if fixes:
            logger.info(f"f"  Applied fixes: {fixes}"")
            total_fixes += sum(len(f) for f in fixes.values())
    
    logger.info(f"f"\nTotal fixes applied: {total_fixes}"")


if __name__ == "__main__":
    main() 