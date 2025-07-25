#!/usr/bin/env python3
"""
Test task for LM Studio integration
"""

import os
import sys
import json
import time
from datetime import datetime

def run():
    """Run LM Studio integration test"""
    print("🤖 Testing LM Studio Integration...")
    
    # Add TokIntel path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    tokintel_path = os.path.join(desktop_path, "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    print(f"[INFO] TokIntel path: {tokintel_path}")
    
    try:
        # Test import
        print("[INFO] Testing imports...")
        from llm.lmstudio_client import create_lmstudio_client
        print("[OK] LM Studio client imported successfully")
        
        # Create client
        print("[INFO] Creating LM Studio client...")
        config = {
            'model': 'mistral',
            'timeout': 30,
            'max_retries': 3
        }
        
        client = create_lmstudio_client(config)
        
        # Test connection
        print("[INFO] Testing server connection...")
        status = client.get_status()
        
        if status['connected']:
            print("  [OK] LM Studio server is running")
            print(f"  [INFO] URL: {status['base_url']}")
            print(f"  🤖 Model: {status['model']}")
            print(f"  ⏱️ Timeout: {status['timeout']}s")
            
            if status['available_models']:
                print(f"  [INFO] Available models: {', '.join(status['available_models'])}")
            else:
                print("  [WARN]️ No models detected")
        else:
            print("  [ERROR] LM Studio server is not running")
            print("  💡 Start LM Studio server and load a model")
            return
        
        # Test simple prompt
        print("\n💬 Testing simple prompt...")
        test_prompt = "What is artificial intelligence in one sentence?"
        
        try:
            result = client.ask(test_prompt)
            
            if result['status'] == 'success':
                print(f"  [OK] Response received!")
                print(f"  [INFO] Prompt: {test_prompt}")
                print(f"  🤖 Response: {result['text']}")
                print(f"  ⏱️ Time: {result['processing_time']:.2f}s")
                print(f"  🏷️ Model: {result['model']}")
            else:
                print(f"  [ERROR] Request failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"  [ERROR] Test failed: {e}")
        
        # Test chat conversation
        print("\n💬 Testing chat conversation...")
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "Can you explain machine learning briefly?"}
        ]
        
        try:
            result = client.chat(messages)
            
            if result['status'] == 'success':
                print(f"  [OK] Chat response received!")
                print(f"  💬 Messages: {len(messages)}")
                print(f"  🤖 Response: {result['text']}")
                print(f"  ⏱️ Time: {result['processing_time']:.2f}s")
            else:
                print(f"  [ERROR] Chat failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"  [ERROR] Chat test failed: {e}")
        
        # Test benchmark
        print("\n⚡ Testing benchmark...")
        test_prompts = [
            "What is Python?",
            "Explain machine learning",
            "How does a neural network work?"
        ]
        
        try:
            benchmark = client.benchmark(test_prompts)
            
            print(f"  [OK] Benchmark completed!")
            print(f"  [REPORT] Total prompts: {benchmark['total_prompts']}")
            print(f"  [OK] Successful: {benchmark['successful']}")
            print(f"  [ERROR] Failed: {benchmark['failed']}")
            print(f"  ⏱️ Total time: {benchmark['total_time']:.2f}s")
            print(f"  [REPORT] Average time: {benchmark['average_time']:.2f}s")
            print(f"  🎯 Success rate: {benchmark['success_rate']:.1f}%")
            
            # Save benchmark result
            reports_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(reports_dir, f"lmstudio_benchmark_{timestamp}.json")
            
            with open(report_path, 'w') as f:
                json.dump(benchmark, f, indent=2)
            
            print(f"  [INFO] Benchmark saved: {report_path}")
            
        except Exception as e:
            print(f"  [ERROR] Benchmark failed: {e}")
        
        # Test different models
        print("\n🏷️ Testing different models...")
        available_models = status.get('available_models', [])
        
        if len(available_models) > 1:
            for model in available_models[:2]:  # Test first 2 models
                try:
                    print(f"  Testing model: {model}")
                    result = client.ask("Hello, this is a test.", model=model)
                    
                    if result['status'] == 'success':
                        print(f"    [OK] {model}: {result['processing_time']:.2f}s")
                    else:
                        print(f"    [ERROR] {model}: {result.get('error', 'Failed')}")
                        
                except Exception as e:
                    print(f"    [ERROR] {model}: {e}")
        else:
            print("  ℹ️ Only one model available, skipping model comparison")
        
        print("\n[INFO] LM Studio integration test completed!")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies:")
        print("  pip install requests")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    run() 