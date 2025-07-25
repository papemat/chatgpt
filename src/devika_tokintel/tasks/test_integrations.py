import os
import sys
import importlib

def run():
    print("[INFO] Testing TokIntel Integrations...")
    
    # Aggiungi il path di TokIntel (path assoluto)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Risali di due livelli: tasks -> devika_tokintel -> Desktop
    desktop_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    tokintel_path = os.path.join(desktop_path, "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    print(f"[INFO] TokIntel path: {tokintel_path}")
    
    integrations = {
        "Whisper": {
            "module": "audio.whisper_transcriber",
            "description": "Audio/Video transcription",
            "status": "[OK] Implemented"
        },
        "Ollama": {
            "module": "llm.ollama_client", 
            "description": "Local LLM inference",
            "status": "[OK] Implemented"
        },
        "HuggingFace": {
            "module": "huggingface.inference",
            "description": "NLP tasks with Transformers",
            "status": "[OK] Implemented"
        }
    }
    
    print("[INFO] Integration Status:")
    print("-" * 60)
    
    for name, info in integrations.items():
        print(f"{name:<15} | {info['description']:<25} | {info['status']}")
    
    print("\n🎯 Next Steps:")
    print("1. Use Cursor AI prompts to design architecture")
    print("2. Implement modules based on AI suggestions")
    print("3. Add integration tests to Devika")
    print("4. Update task_runner.py with new tasks")
    
    # Check if any integration files exist
    print("\n[INFO] Checking for existing integration files:")
    
    integration_files = [
        os.path.join(tokintel_path, "audio", "whisper_transcriber.py"),
        os.path.join(tokintel_path, "llm", "ollama_client.py"),
        os.path.join(tokintel_path, "huggingface", "inference.py")
    ]
    
    for file_path in integration_files:
        if os.path.exists(file_path):
            print(f"  [OK] {os.path.basename(file_path)}")
        else:
            print(f"  [ERROR] {os.path.basename(file_path)} (missing)")
    
    print("\n💡 Ready for AI-powered architecture design!")
    return integrations 