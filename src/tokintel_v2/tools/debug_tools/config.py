#!/usr/bin/env python3
"""
TokIntel v2 - Debug Tools Configuration
Configurazione per i tool di audit e debug
"""


class DebugConfig:
    """Configuration for debug tools"""
    
    # Directories to exclude from audit
    EXCLUDE_DIRS = [
        '__pycache__',
        '.git',
        'venv',
        'env',
        '.pytest_cache',
        'node_modules',
        'build',
        'dist'
    ]
    
    # File extensions to audit
    AUDIT_EXTENSIONS = ['.py']
    
    # Tools configuration
    TOOLS = {
        'black': {
            'enabled': True,
            'line_length': 88,
            'target_version': 'py39'
        },
        'flake8': {
            'enabled': True,
            'max_line_length': 88,
            'ignore': ['E203', 'W503']
        },
        'mypy': {
            'enabled': True,
            'strict': False,
            'ignore_missing_imports': True
        },
        'autoflake': {
            'enabled': True,
            'remove_all_unused_imports': True,
            'remove_unused_variables': True
        }
    }
    
    # Warning patterns to check
    WARNING_PATTERNS = [
        (r'import\s+\*', "Wildcard imports detected"),
        (r'except\s*:', "Bare except clauses detected"),
        (r'print\s*\(', "Print statements detected (use logger instead)"),
        (r'input\s*\(', "Input statements detected (security concern)"),
        (r'eval\s*\(', "Eval statements detected (security concern)"),
        (r'exec\s*\(', "Exec statements detected (security concern)"),
        (r'assert\s+', "Assert statements in production code"),
        (r'# TODO:', "TODO comments found"),
        (r'# FIXME:', "FIXME comments found"),
        (r'# HACK:', "HACK comments found"),
    ]
    
    # Async patterns to check
    ASYNC_PATTERNS = [
        (r'async def.*\n.*await', "Async function with await"),
        (r'await.*\n.*async def', "Await outside async function"),
        (r'asyncio\.run.*asyncio\.run', "Nested asyncio.run calls"),
        (r'asyncio\.get_event_loop\(\)', "Deprecated asyncio.get_event_loop()"),
        (r'loop\.run_until_complete', "Deprecated run_until_complete"),
    ]
    
    # Security patterns to check
    SECURITY_PATTERNS = [
        (r'password\s*=\s*["\'][^"\']*["\']', "Hardcoded password detected"),
        (r'api_key\s*=\s*["\'][^"\']*["\']', "Hardcoded API key detected"),
        (r'secret\s*=\s*["\'][^"\']*["\']', "Hardcoded secret detected"),
        (r'token\s*=\s*["\'][^"\']*["\']', "Hardcoded token detected"),
        (r'\.env', "Environment file reference"),
        (r'os\.system\s*\(', "os.system() detected (use subprocess instead)"),
        (r'subprocess\.call\s*\(', "subprocess.call() detected (security concern)"),
    ]
    
    # Performance patterns to check
    PERFORMANCE_PATTERNS = [
        (r'for.*in.*range\(len\(', "Inefficient loop with range(len())"),
        (r'\.append\(.*\)\s*in\s*loop', "List append in loop (consider list comprehension)"),
        (r'import\s+.*\s+as\s+.*\s+import\s+', "Multiple imports on same line"),
        (r'def\s+\w+\(.*\):\s*\n\s*pass', "Empty function definition"),
    ]
    
    # Report settings
    REPORT_SETTINGS = {
        'max_warnings_display': 10,
        'max_errors_display': 10,
        'max_fixes_display': 10,
        'save_report': True,
        'report_format': 'json',  # 'json' or 'txt'
        'include_timestamp': True,
        'include_file_stats': True
    }
    
    @classmethod
    def get_tool_config(cls, tool_name: str) -> Dict[str, Any]:
        """Get configuration for a specific tool"""
        return cls.TOOLS.get(tool_name, {})
    
    @classmethod
    def is_tool_enabled(cls, tool_name: str) -> bool:
        """Check if a tool is enabled"""
        return cls.TOOLS.get(tool_name, {}).get('enabled', False)
    
    @classmethod
    def get_patterns(cls, pattern_type: str) -> List[tuple]:
        """Get patterns of a specific type"""
        pattern_map = {
            'warning': cls.WARNING_PATTERNS,
            'async': cls.ASYNC_PATTERNS,
            'security': cls.SECURITY_PATTERNS,
            'performance': cls.PERFORMANCE_PATTERNS
        }
        return pattern_map.get(pattern_type, [])
    
    @classmethod
    def should_exclude_dir(cls, dir_name: str) -> bool:
        """Check if directory should be excluded"""
        return dir_name in cls.EXCLUDE_DIRS
    
    @classmethod
    def should_audit_file(cls, file_path: Path) -> bool:
        """Check if file should be audited"""
        return file_path.suffix in cls.AUDIT_EXTENSIONS 