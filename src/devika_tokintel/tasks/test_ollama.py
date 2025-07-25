import os
import sys
import json
from datetime import datetime

def run():
    print("🤖 Testing Ollama Integration...")
    
    # Aggiungi il path di TokIntel (path assoluto)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Risali di due livelli: tasks -> devika_tokintel -> Desktop
    desktop_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    tokintel_path = os.path.join(desktop_path, "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    print(f"[INFO] TokIntel path: {tokintel_path}")
    
    try:
        # Test import
        print("[INFO] Testing imports...")
        from llm.ollama_client import create_ollama_client
        
        # Test configuration
        config = {
            'base_url': 'http://localhost:11434',
            'default_model': 'mistral',
            'timeout': 30,
            'max_retries': 3,
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        print("[INFO] Creating Ollama client...")
        client = create_ollama_client(config)
        
        # Test server connection
        print("[INFO] Testing server connection...")
        if client.is_server_running():
            print("  [OK] Ollama server is running")
        else:
            print("  [ERROR] Ollama server is not running")
            print("  💡 Start Ollama server: ollama serve")
            return
        
        # Test available models
        print("[INFO] Checking available models...")
        models = client.get_models()
        if models:
            print(f"  Available models: {', '.join(models)}")
        else:
            print("  No models available")
            print("  💡 Pull a model: ollama pull mistral")
            return
        
        # Test status
        print("[REPORT] Checking client status...")
        status = client.get_status()
        
        print(f"  Server running: {status['server_running']}")
        print(f"  Base URL: {status['base_url']}")
        print(f"  Default model: {status['default_model']}")
        print(f"  Available models: {len(status['available_models'])}")
        print(f"  Timeout: {status['timeout']}s")
        print(f"  Max retries: {status['max_retries']}")
        
        # Test text generation
        print(f"\n💬 Testing text generation...")
        test_prompt = "Explain artificial intelligence in simple terms."
        
        try:
            result = client.generate(test_prompt)
            print(f"  [OK] Generation successful!")
            print(f"  Model: {result['model']}")
            print(f"  Response: {result['text'][:100]}...")
            print(f"  Tokens: {result['usage']['total_tokens']}")
            print(f"  Temperature: {result['temperature']}")
            
            # Save result
            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(reports_dir, f"ollama_test_{timestamp}.json")
            
            with open(report_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"  [INFO] Result saved: {report_path}")
            
        except Exception as e:
            print(f"  [ERROR] Generation failed: {e}")
        
        # Test chat completion
        print(f"\n💭 Testing chat completion...")
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you!"},
            {"role": "user", "content": "What can you help me with?"}
        ]
        
        try:
            result = client.chat(messages)
            print(f"  [OK] Chat completion successful!")
            print(f"  Model: {result['model']}")
            print(f"  Response: {result['text'][:100]}...")
            print(f"  Tokens: {result['usage']['total_tokens']}")
            
        except Exception as e:
            print(f"  [ERROR] Chat completion failed: {e}")
        
        # Test embeddings
        print(f"\n[INFO] Testing embeddings...")
        test_text = "This is a test text for embeddings."
        
        try:
            embeddings = client.embed(test_text)
            print(f"  [OK] Embeddings generated!")
            print(f"  Dimensions: {len(embeddings)}")
            print(f"  Sample values: {embeddings[:5]}")
            
        except Exception as e:
            print(f"  [ERROR] Embeddings failed: {e}")
        
        # Test benchmark
        print(f"\n⚡ Testing benchmark...")
        test_prompts = [
            "Explain quantum computing.",
            "Write a short poem about AI.",
            "What are renewable energy sources?"
        ]
        
        try:
            benchmark = client.benchmark_model('mistral', test_prompts)
            print(f"  [OK] Benchmark completed!")
            print(f"  Model: {benchmark['model']}")
            print(f"  Test prompts: {benchmark['test_prompts']}")
            print(f"  Successful tests: {benchmark['successful_tests']}")
            print(f"  Total tokens: {benchmark['total_tokens']}")
            print(f"  Total time: {benchmark['total_time']:.2f}s")
            print(f"  Avg tokens/sec: {benchmark['average_tokens_per_second']:.2f}")
            
            # Save benchmark
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            benchmark_path = os.path.join(reports_dir, f"ollama_benchmark_{timestamp}.json")
            
            with open(benchmark_path, 'w') as f:
                json.dump(benchmark, f, indent=2)
            
            print(f"  [INFO] Benchmark saved: {benchmark_path}")
            
        except Exception as e:
            print(f"  [ERROR] Benchmark failed: {e}")
        
        # Test model pulling (optional)
        print(f"\n[INFO] Testing model pulling...")
        test_model = "llama2:7b"
        
        try:
            if test_model not in models:
                print(f"  Pulling model: {test_model}")
                success = client.pull_model(test_model)
                if success:
                    print(f"  [OK] Model {test_model} pulled successfully")
                else:
                    print(f"  [ERROR] Failed to pull model {test_model}")
            else:
                print(f"  Model {test_model} already available")
                
        except Exception as e:
            print(f"  [ERROR] Model pulling failed: {e}")
        
        print(f"\n[INFO] Ollama integration test completed!")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies:")
        print("  pip install requests")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    run() 