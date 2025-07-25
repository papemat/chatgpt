import os
import sys
import platform
import psutil
import yaml
from datetime import datetime

def run():
    print("🏥 Running TokIntel System Health Check...")
    
    # Aggiungi il path di TokIntel
    tokintel_path = os.path.join(os.path.dirname(__file__), "..", "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    health_report = {
        'timestamp': datetime.now().isoformat(),
        'system': {},
        'tokintel': {},
        'dependencies': {},
        'issues': []
    }
    
    # System Info
    print("💻 System Information:")
    health_report['system'] = {
        'platform': platform.system(),
        'version': platform.version(),
        'python_version': sys.version,
        'cpu_count': psutil.cpu_count(),
        'memory_total': f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
        'memory_available': f"{psutil.virtual_memory().available / (1024**3):.1f} GB"
    }
    
    print(f"  OS: {health_report['system']['platform']} {health_report['system']['version']}")
    print(f"  Python: {health_report['system']['python_version'].split()[0]}")
    print(f"  CPU: {health_report['system']['cpu_count']} cores")
    print(f"  Memory: {health_report['system']['memory_available']} available / {health_report['system']['memory_total']} total")
    
    # TokIntel Structure Check
    print("\n[INFO] TokIntel Structure Check:")
    required_dirs = ['agents', 'core', 'llm', 'ui', 'config', 'output', 'logs']
    required_files = ['config.yaml', 'main.py', 'requirements.txt']
    
    for dir_name in required_dirs:
        dir_path = os.path.join(tokintel_path, dir_name)
        if os.path.exists(dir_path):
            print(f"  [OK] {dir_name}/")
            health_report['tokintel'][f'dir_{dir_name}'] = 'OK'
        else:
            print(f"  [ERROR] {dir_name}/ (missing)")
            health_report['tokintel'][f'dir_{dir_name}'] = 'MISSING'
            health_report['issues'].append(f"Missing directory: {dir_name}")
    
    for file_name in required_files:
        file_path = os.path.join(tokintel_path, file_name)
        if os.path.exists(file_path):
            print(f"  [OK] {file_name}")
            health_report['tokintel'][f'file_{file_name}'] = 'OK'
        else:
            print(f"  [ERROR] {file_name} (missing)")
            health_report['tokintel'][f'file_{file_name}'] = 'MISSING'
            health_report['issues'].append(f"Missing file: {file_name}")
    
    # Config Validation
    print("\n⚙️ Configuration Check:")
    config_path = os.path.join(tokintel_path, "config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check required config sections
            required_sections = ['llm', 'agents', 'ui']
            for section in required_sections:
                if section in config:
                    print(f"  [OK] {section} section")
                    health_report['tokintel'][f'config_{section}'] = 'OK'
                else:
                    print(f"  [WARN]️ {section} section (missing)")
                    health_report['tokintel'][f'config_{section}'] = 'MISSING'
                    health_report['issues'].append(f"Missing config section: {section}")
            
            # Check API keys
            llm_config = config.get('llm', {})
            api_keys_found = 0
            for model, model_config in llm_config.items():
                if isinstance(model_config, dict) and 'api_key' in model_config:
                    api_keys_found += 1
            
            if api_keys_found > 0:
                print(f"  [OK] {api_keys_found} API keys configured")
                health_report['tokintel']['api_keys'] = f'{api_keys_found} configured'
            else:
                print(f"  [WARN]️ No API keys found")
                health_report['tokintel']['api_keys'] = 'NONE'
                health_report['issues'].append("No API keys configured")
                
        except Exception as e:
            print(f"  [ERROR] Config error: {e}")
            health_report['tokintel']['config_valid'] = 'ERROR'
            health_report['issues'].append(f"Config error: {e}")
    else:
        print(f"  [ERROR] config.yaml not found")
        health_report['tokintel']['config_valid'] = 'MISSING'
        health_report['issues'].append("config.yaml not found")
    
    # Dependencies Check
    print("\n[INFO] Dependencies Check:")
    try:
        import requests
        print("  [OK] requests")
        health_report['dependencies']['requests'] = 'OK'
    except ImportError:
        print("  [ERROR] requests (missing)")
        health_report['dependencies']['requests'] = 'MISSING'
        health_report['issues'].append("Missing dependency: requests")
    
    try:
        import openai
        print("  [OK] openai")
        health_report['dependencies']['openai'] = 'OK'
    except ImportError:
        print("  [WARN]️ openai (missing)")
        health_report['dependencies']['openai'] = 'MISSING'
        health_report['issues'].append("Missing dependency: openai")
    
    try:
        import streamlit
        print("  [OK] streamlit")
        health_report['dependencies']['streamlit'] = 'OK'
    except ImportError:
        print("  [WARN]️ streamlit (missing)")
        health_report['dependencies']['streamlit'] = 'MISSING'
        health_report['issues'].append("Missing dependency: streamlit")
    
    # Performance Check
    print("\n⚡ Performance Check:")
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    
    print(f"  CPU Usage: {cpu_usage:.1f}%")
    print(f"  Memory Usage: {memory_usage:.1f}%")
    
    health_report['system']['cpu_usage'] = cpu_usage
    health_report['system']['memory_usage'] = memory_usage
    
    if memory_usage > 90:
        health_report['issues'].append("High memory usage")
        print("  [WARN]️ High memory usage detected")
    
    if cpu_usage > 90:
        health_report['issues'].append("High CPU usage")
        print("  [WARN]️ High CPU usage detected")
    
    # Summary
    print(f"\n[REPORT] Health Summary:")
    total_checks = len(health_report['tokintel']) + len(health_report['dependencies'])
    passed_checks = sum(1 for v in health_report['tokintel'].values() if v == 'OK') + \
                   sum(1 for v in health_report['dependencies'].values() if v == 'OK')
    
    print(f"  Checks passed: {passed_checks}/{total_checks}")
    print(f"  Issues found: {len(health_report['issues'])}")
    
    if health_report['issues']:
        print(f"\n[WARN]️ Issues detected:")
        for issue in health_report['issues']:
            print(f"  - {issue}")
    else:
        print(f"\n[INFO] All systems operational!")
    
    # Save report
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"health_report_{timestamp}.json")
    
    import json
    with open(report_path, 'w') as f:
        json.dump(health_report, f, indent=2)
    
    print(f"\n[INFO] Health report saved: {report_path}")
    
    return health_report 