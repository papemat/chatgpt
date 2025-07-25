#!/usr/bin/env python3
"""
TokIntel v2 - Post-Audit Validator
Controllo approfondito post-audit per validare coerenza, edge case e regressioni
"""

import ast
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostAuditValidator:
    """Validator per controlli post-audit approfonditi"""
    
    def __init__(self, project_root: str = "."):
        """Initialize validator"""
        self.project_root = Path(project_root)
        self.python_files = []
        self.report = {
            "typing_inconsistencies": [],
            "docstring_issues": [],
            "missing_tests": [],
            "edge_cases": [],
            "tool_validation": [],
            "coupling_issues": [],
            "error_handling": [],
            "performance_issues": []
        }
        self._discover_python_files()
    
    def _discover_python_files(self):
        """Discover all Python files"""
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
            for file in files:
                if file.endswith('.py'):
                    self.python_files.append(Path(root) / file)
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete post-audit validation"""
        logger.info("Starting post-audit validation...")
        
        try:
            # 1. Check typing consistency
            self._check_typing_consistency()
            
            # 2. Check docstring issues
            self._check_docstring_issues()
            
            # 3. Check missing tests
            self._check_missing_tests()
            
            # 4. Check edge cases
            self._check_edge_cases()
            
            # 5. Validate audit tools
            self._validate_audit_tools()
            
            # 6. Check coupling issues
            self._check_coupling_issues()
            
            # 7. Check error handling
            self._check_error_handling()
            
            # 8. Check performance issues
            self._check_performance_issues()
            
            logger.info("Post-audit validation completed")
            return self.report
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            self.report["tool_validation"].append(f"Validation failed: {e}")
            return self.report
    
    def _check_typing_consistency(self):
        """Check consistency between typing, docstring and implementation"""
        logger.info("Checking typing consistency...")
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check function typing
                        self._validate_function_typing(node, py_file, content)
                    elif isinstance(node, ast.ClassDef):
                        # Check class typing
                        self._validate_class_typing(node, py_file, content)
                        
            except Exception as e:
                self.report["typing_inconsistencies"].append(f"Error parsing {py_file}: {e}")
    
    def _validate_function_typing(self, node: ast.FunctionDef, file_path: Path, content: str):
        """Validate function typing consistency"""
        func_name = node.name
        
        # Check if function has type hints
        has_return_type = node.returns is not None
        has_param_types = any(arg.annotation is not None for arg in node.args.args)
        
        # Check docstring
        docstring = ast.get_docstring(node)
        
        # Check for typing inconsistencies
        if has_param_types and docstring:
            # Check if docstring mentions types that don't match annotations
            param_types_in_doc = self._extract_param_types_from_docstring(docstring)
            param_types_in_code = self._extract_param_types_from_annotations(node.args.args)
            
            for param, doc_type in param_types_in_doc.items():
                if param in param_types_in_code:
                    code_type = param_types_in_code[param]
                    if not self._types_compatible(doc_type, code_type):
                        self.report["typing_inconsistencies"].append(
                            f"Type mismatch in {file_path}:{node.lineno} - {func_name}.{param}: "
                            f"docstring says {doc_type}, code says {code_type}"
                        )
        
        # Check for missing return type hints
        if not has_return_type and docstring and "return" in docstring.lower():
            self.report["typing_inconsistencies"].append(
                f"Missing return type hint in {file_path}:{node.lineno} - {func_name}"
            )
    
    def _validate_class_typing(self, node: ast.ClassDef, file_path: Path, content: str):
        """Validate class typing consistency"""
        class_name = node.name
        
        # Check class docstring
        docstring = ast.get_docstring(node)
        
        # Check for class attributes without type hints
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and item.target:
                # Has type annotation
                pass
            elif isinstance(item, ast.Assign) and docstring:
                # Check if assignment is documented in docstring
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attr_name = target.id
                        if not self._attribute_documented_in_docstring(attr_name, docstring):
                            self.report["typing_inconsistencies"].append(
                                f"Undocumented class attribute in {file_path}:{item.lineno} - {class_name}.{attr_name}"
                            )
    
    def _check_docstring_issues(self):
        """Check for docstring issues"""
        logger.info("Checking docstring issues...")
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        docstring = ast.get_docstring(node)
                        if docstring:
                            # Check for common docstring issues
                            self._validate_docstring_quality(docstring, node, py_file)
                        else:
                            # Check if function/class should have docstring
                            if self._should_have_docstring(node):
                                self.report["docstring_issues"].append(
                                    f"Missing docstring in {py_file}:{node.lineno} - {node.name}"
                                )
                                
            except Exception as e:
                self.report["docstring_issues"].append(f"Error checking docstrings in {py_file}: {e}")
    
    def _check_missing_tests(self):
        """Check for missing tests in critical modules"""
        logger.info("Checking missing tests...")
        
        critical_modules = [
            'core/config.py',
            'core/logger.py', 
            'agents/pipeline.py',
            'llm/handler.py',
            'utils/file_utils.py'
        ]
        
        test_files = [f for f in self.python_files if 'test' in f.name.lower()]
        
        for module in critical_modules:
            module_path = self.project_root / module
            if module_path.exists():
                # Check if there's a corresponding test file
                test_file = self._find_test_file(module_path, test_files)
                if not test_file:
                    self.report["missing_tests"].append(
                        f"Missing tests for critical module: {module}"
                    )
    
    def _check_edge_cases(self):
        """Check for potential edge cases not covered by syntax audit"""
        logger.info("Checking edge cases...")
        
        edge_case_patterns = [
            (r'\.get\([^)]*\)\s*\[', "Dictionary access after .get() without None check"),
            (r'for\s+\w+\s+in\s+\w+\.values\(\)\s*:', "Iterating over dict.values() without checking if dict is empty"),
            (r'len\([^)]*\)\s*==\s*0', "Length comparison instead of truthiness check"),
            (r'if\s+\w+\s*is\s*None\s*and\s*\w+', "Complex None checks that might be simplified"),
            (r'except\s+\w+Exception\s*:', "Broad exception catching"),
        ]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, message in edge_case_patterns:
                    if re.search(pattern, content):
                        self.report["edge_cases"].append(
                            f"Potential edge case in {py_file}: {message}"
                        )
                        
            except Exception as e:
                self.report["edge_cases"].append(f"Error checking edge cases in {py_file}: {e}")
    
    def _validate_audit_tools(self):
        """Validate that audit tools don't have issues"""
        logger.info("Validating audit tools...")
        
        audit_tools = [
            'tools/debug_tools/audit_script.py',
            'tools/debug_tools/fixes.py',
            'tools/debug_tools/config.py'
        ]
        
        for tool in audit_tools:
            tool_path = self.project_root / tool
            if tool_path.exists():
                # Check for hardcoded paths
                with open(tool_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for hardcoded paths
                if re.search(r'TokIntel_v2', content):
                    self.report["tool_validation"].append(
                        f"Hardcoded path in {tool}: 'TokIntel_v2'"
                    )
                
                # Check for broken f-strings
                if re.search(r'f"[^"]*\{[^}]*"[^"]*"', content):
                    self.report["tool_validation"].append(
                        f"Potential broken f-string in {tool}"
                    )
                
                # Check for side effects (writing outside output/)
                if re.search(r'open\([^)]*["\'](?!output/)', content):
                    self.report["tool_validation"].append(
                        f"Potential side effect in {tool}: writing outside output/"
                    )
    
    def _check_coupling_issues(self):
        """Check for tight coupling between modules"""
        logger.info("Checking coupling issues...")
        
        # Analyze imports to find coupling
        module_imports = {}
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                
                module_imports[str(py_file)] = imports
                
            except Exception as e:
                self.report["coupling_issues"].append(f"Error analyzing imports in {py_file}: {e}")
        
        # Check for circular imports
        self._check_circular_imports(module_imports)
        
        # Check for too many imports
        for module, imports in module_imports.items():
            if len(imports) > 15:  # Threshold for too many imports
                self.report["coupling_issues"].append(
                    f"Too many imports in {module}: {len(imports)} imports"
                )
    
    def _check_error_handling(self):
        """Check for missing error handling"""
        logger.info("Checking error handling...")
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Check for risky function calls without error handling
                        if isinstance(node.func, ast.Attribute):
                            func_name = node.func.attr
                            if func_name in ['open', 'requests.get', 'subprocess.run']:
                                # Check if this call is in a try-except block
                                if not self._is_in_try_except(node, tree):
                                    self.report["error_handling"].append(
                                        f"Risky function call without error handling in {py_file}:{node.lineno} - {func_name}"
                                    )
                                    
            except Exception as e:
                self.report["error_handling"].append(f"Error checking error handling in {py_file}: {e}")
    
    def _check_performance_issues(self):
        """Check for potential performance issues"""
        logger.info("Checking performance issues...")
        
        performance_patterns = [
            (r'for\s+\w+\s+in\s+range\(len\([^)]*\)\)', "Inefficient loop with range(len())"),
            (r'\.append\([^)]*\)\s*in\s*loop', "List append in loop - consider list comprehension"),
            (r'import\s+\*', "Wildcard import - performance impact"),
            (r'def\s+\w+\([^)]*\):\s*\n\s*pass', "Empty function - potential performance overhead"),
        ]
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, message in performance_patterns:
                    if re.search(pattern, content):
                        self.report["performance_issues"].append(
                            f"Performance issue in {py_file}: {message}"
                        )
                        
            except Exception as e:
                self.report["performance_issues"].append(f"Error checking performance in {py_file}: {e}")
    
    # Helper methods
    def _extract_param_types_from_docstring(self, docstring: str) -> Dict[str, str]:
        """Extract parameter types from docstring"""
        types = {}
        # Simple regex to find param types in docstring
        param_pattern = r':param\s+(\w+):\s*([^:]+)'
        for match in re.finditer(param_pattern, docstring):
            param_name, param_desc = match.groups()
            # Extract type from description
            type_match = re.search(r'(\w+(?:\[\w+\])?)', param_desc)
            if type_match:
                types[param_name] = type_match.group(1)
        return types
    
    def _extract_param_types_from_annotations(self, args: List[ast.arg]) -> Dict[str, str]:
        """Extract parameter types from function annotations"""
        types = {}
        for arg in args:
            if arg.annotation:
                types[arg.arg] = ast.unparse(arg.annotation)
        return types
    
    def _types_compatible(self, doc_type: str, code_type: str) -> bool:
        """Check if types are compatible"""
        # Simple type compatibility check
        type_mapping = {
            'str': 'string',
            'int': 'integer',
            'list': 'array',
            'dict': 'dictionary',
            'bool': 'boolean',
        }
        
        doc_type_lower = doc_type.lower()
        code_type_lower = code_type.lower()
        
        # Direct match
        if doc_type_lower == code_type_lower:
            return True
        
        # Check mapping
        for code_t, doc_t in type_mapping.items():
            if (doc_type_lower == doc_t and code_type_lower == code_t) or \
               (code_type_lower == doc_t and doc_type_lower == code_t):
                return True
        
        return False
    
    def _should_have_docstring(self, node: ast.AST) -> bool:
        """Check if node should have a docstring"""
        # Public functions and classes should have docstrings
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return not node.name.startswith('_')
        return False
    
    def _find_test_file(self, module_path: Path, test_files: List[Path]) -> Optional[Path]:
        """Find corresponding test file for a module"""
        module_name = module_path.stem
        for test_file in test_files:
            if module_name in test_file.name:
                return test_file
        return None
    
    def _is_in_try_except(self, node: ast.AST, tree: ast.AST) -> bool:
        """Check if node is inside a try-except block"""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.Try):
                if node in ast.walk(parent):
                    return True
        return False
    
    def _check_circular_imports(self, module_imports: Dict[str, List[str]]):
        """Check for circular imports"""
        # Simple circular import detection
        for module, imports in module_imports.items():
            for imported_module in imports:
                if imported_module in module_imports:
                    if module in module_imports[imported_module]:
                        self.report["coupling_issues"].append(
                            f"Circular import detected: {module} ↔ {imported_module}"
                        )
    
    def _attribute_documented_in_docstring(self, attr_name: str, docstring: str) -> bool:
        """Check if class attribute is documented in docstring"""
        return attr_name in docstring
    
    def _validate_docstring_quality(self, docstring: str, node: ast.AST, py_file: Path):
        """Validate docstring quality"""
        # Check for common docstring issues
        if len(docstring.strip()) < 10:
            self.report["docstring_issues"].append(
                f"Very short docstring in {py_file}:{node.lineno} - {getattr(node, 'name', 'unknown')}"
            )
        
        # Check for missing parameter documentation
        if isinstance(node, ast.FunctionDef) and node.args.args:
            for arg in node.args.args:
                if arg.arg != 'self' and arg.arg not in docstring:
                    self.report["docstring_issues"].append(
                        f"Missing parameter documentation in {py_file}:{node.lineno} - {node.name}.{arg.arg}"
                    )
    
    def print_summary(self):
        """Print validation summary"""
        logger.info("\n" + "="*60)
        logger.info("TOKINTEL V2 POST-AUDIT VALIDATION SUMMARY")
        logger.info("="*60)
        
        total_issues = sum(len(issues) for issues in self.report.values())
        logger.info(f"Python files validated: {len(self.python_files)}")
        logger.info(f"Total issues found: {total_issues}")
        
        for category, issues in self.report.items():
            if issues:
                logger.info(f"\n{category.upper().replace('_', ' ')} ({len(issues)}):")
                for issue in issues[:3]:  # Show first 3
                    logger.info(f"  - {issue}")
                if len(issues) > 3:
                    logger.info(f"  ... and {len(issues) - 3} more")
        
        logger.info("\n" + "="*60)

def main():
    """Main function"""
    logger.info("TokIntel v2 - Post-Audit Validator")
    logger.info("="*40)
    
    validator = PostAuditValidator()
    report = validator.run_full_validation()
    
    validator.print_summary()
    
    # Save report
    import json
    with open('post_audit_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info("Post-audit report saved to: post_audit_report.json")

if __name__ == "__main__":
    main() 