#!/usr/bin/env python3
"""
Centralized task runner for Devika
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import all task modules
try:
    from . import test_config, refactor_prompt, retry_logic, test_agents, benchmark_llm, export_csv, system_health, auto_maintenance, test_integrations, test_whisper, test_ollama, test_huggingface, test_lmstudio, test_model_management
except ImportError as e:
    print(f"Warning: Some tasks could not be imported: {e}")

# Define available tasks
tasks = {
    "test_config": test_config.run,
    "refactor_prompt": refactor_prompt.run,
    "retry_logic": retry_logic.run,
    "test_agents": test_agents.run,
    "benchmark_llm": benchmark_llm.run,
    "export_csv": export_csv.run,
    "system_health": system_health.run,
    "auto_maintenance": auto_maintenance.run,
    "test_integrations": test_integrations.run,
    "test_whisper": test_whisper.run,
    "test_ollama": test_ollama.run,
    "test_huggingface": test_huggingface.run,
    "test_lmstudio": test_lmstudio.run,
    "test_model_management": test_model_management.run
}

def run(task_name: str):
    """Run a specific task by name (compatibility function)"""
    if task_name in tasks:
        print(f"[INFO] Running task: {task_name}")
        print("=" * 50)
        try:
            tasks[task_name]()
        except Exception as e:
            print(f"[ERROR] Task {task_name} failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"[ERROR] Task '{task_name}' not found")
        print(f"Available tasks: {', '.join(tasks.keys())}")

def run_task(task_name: str):
    """Run a specific task by name (new function)"""
    return run(task_name)

def list_tasks():
    """List all available tasks"""
    print("[INFO] Available Tasks:")
    print("=" * 30)
    for task_name in sorted(tasks.keys()):
        print(f"  • {task_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_name = sys.argv[1]
        run_task(task_name)
    else:
        list_tasks()
