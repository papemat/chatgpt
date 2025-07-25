import os
import sys
import importlib.util

def run():
    print("🤖 Testing TokIntel agents...")
    
    # Aggiungi il path di TokIntel
    tokintel_path = os.path.join(os.path.dirname(__file__), "..", "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    agents_to_test = [
        "agents.scraper_agent",
        "agents.audio_agent", 
        "agents.vision_agent",
        "agents.text_agent"
    ]
    
    results = {}
    
    for agent_name in agents_to_test:
        try:
            print(f"  Testing {agent_name}...")
            module = importlib.import_module(agent_name)
            
            # Verifica se ha i metodi essenziali
            if hasattr(module, 'process') or hasattr(module, 'run'):
                results[agent_name] = "[OK] OK"
                print(f"    [OK] {agent_name} loaded successfully")
            else:
                results[agent_name] = "[WARN]️ Missing process/run method"
                print(f"    [WARN]️ {agent_name} missing essential methods")
                
        except ImportError as e:
            results[agent_name] = f"[ERROR] Import error: {e}"
            print(f"    [ERROR] {agent_name} import failed: {e}")
        except Exception as e:
            results[agent_name] = f"[ERROR] Error: {e}"
            print(f"    [ERROR] {agent_name} error: {e}")
    
    print("\n[REPORT] Agent Test Results:")
    for agent, status in results.items():
        print(f"  {agent}: {status}")
    
    # Conta successi
    success_count = sum(1 for status in results.values() if "[OK]" in status)
    total_count = len(results)
    
    print(f"\n🎯 Summary: {success_count}/{total_count} agents working")
    
    if success_count == total_count:
        print("[INFO] All agents are ready!")
    else:
        print("[WARN]️ Some agents need attention") 