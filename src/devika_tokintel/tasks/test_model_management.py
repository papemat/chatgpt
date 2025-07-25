#!/usr/bin/env python3
"""
Test task for automatic model management
Tests ensure_model functionality for LM Studio and Ollama
"""
import os
import sys
import json
import time
from datetime import datetime

def run():
    print("[INFO] Testing Automatic Model Management...")
    print("=" * 60)
    
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    tokintel_path = os.path.join(desktop_path, "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    try:
        from utils.llm_router import create_llm_router, load_config_from_file
        
        # Load configuration
        config_path = os.path.join(tokintel_path, "config_integrations.yaml")
        if os.path.exists(config_path):
            config = load_config_from_file(config_path)
            llm_config = config.get('llm', {})
        else:
            print("[WARN]️  Config file not found, using default settings")
            llm_config = {
                "preferred_backend": "lmstudio",
                "fallback_strategy": "auto",
                "lmstudio": {
                    "base_url": "http://localhost:1234/v1/chat/completions",
                    "model": "mistral"
                },
                "ollama": {
                    "base_url": "http://localhost:11434",
                    "model": "mistral"
                }
            }
        
        # Create router
        print("[INFO] Initializing LLM Router...")
        router = create_llm_router(llm_config)
        
        # Get initial status
        status = router.get_status()
        print(f"[REPORT] Initial Router Status:")
        print(f"   Current Backend: {status.get('current_backend', 'None')}")
        print(f"   Available Backends: {status.get('available_backends', [])}")
        
        # Test models to check
        test_models = [
            "mistral",
            "llama2",
            "llama3",
            "gemma",
            "codellama"
        ]
        
        print(f"\n[INFO] Testing Model Management for {len(test_models)} models...")
        print("=" * 60)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "test_models": test_models,
            "backends": {},
            "summary": {}
        }
        
        # Test each backend
        for backend in router.clients.keys():
            print(f"\n🤖 Testing {backend.upper()} Backend:")
            print("-" * 40)
            
            backend_results = {
                "backend": backend,
                "models": {},
                "summary": {
                    "total_models": len(test_models),
                    "available_models": 0,
                    "unavailable_models": 0,
                    "success_rate": 0
                }
            }
            
            for model in test_models:
                print(f"   [INFO] Testing model: {model}")
                
                try:
                    # Test ensure_model
                    model_status = router.ensure_model(model, backend)
                    
                    backend_results["models"][model] = model_status
                    
                    if model_status.get("success"):
                        print(f"      [OK] Available")
                        backend_results["summary"]["available_models"] += 1
                    else:
                        print(f"      [WARN]️  Not available")
                        backend_results["summary"]["unavailable_models"] += 1
                        
                        # Show instructions if available
                        if model_status.get("instructions"):
                            print(f"      [INFO] Instructions available ({len(model_status['instructions'])} steps)")
                    
                    # Show actions taken
                    actions = model_status.get("actions_taken", [])
                    if actions:
                        print(f"      [INFO] Actions: {', '.join(actions)}")
                    
                except Exception as e:
                    print(f"      [ERROR] Error: {e}")
                    backend_results["models"][model] = {
                        "success": False,
                        "error": str(e)
                    }
                    backend_results["summary"]["unavailable_models"] += 1
                
                time.sleep(0.5)  # Brief delay between tests
            
            # Calculate success rate
            total = backend_results["summary"]["total_models"]
            available = backend_results["summary"]["available_models"]
            backend_results["summary"]["success_rate"] = (available / total * 100) if total > 0 else 0
            
            print(f"\n   [REPORT] {backend.upper()} Summary:")
            print(f"      Available: {available}/{total} ({backend_results['summary']['success_rate']:.1f}%)")
            
            results["backends"][backend] = backend_results
        
        # Overall summary
        print(f"\n🏆 Overall Summary:")
        print("=" * 60)
        
        total_backends = len(results["backends"])
        total_models = len(test_models)
        
        for backend, backend_results in results["backends"].items():
            summary = backend_results["summary"]
            print(f"🤖 {backend.upper()}: {summary['available_models']}/{total_models} models available ({summary['success_rate']:.1f}%)")
        
        # Test specific model download scenarios
        print(f"\n[INFO] Testing Model Download Scenarios...")
        print("=" * 60)
        
        # Test with a specific model that might not be available
        test_download_model = "llama3"
        print(f"[INFO] Testing download scenario for '{test_download_model}':")
        
        for backend in router.clients.keys():
            print(f"\n   🤖 {backend.upper()}:")
            
            try:
                model_status = router.ensure_model(test_download_model, backend)
                
                if model_status.get("success"):
                    print(f"      [OK] Model is available")
                else:
                    print(f"      [WARN]️  Model not available")
                    
                    # Show detailed instructions
                    instructions = model_status.get("instructions", [])
                    if instructions:
                        print(f"      [INFO] Download Instructions:")
                        for i, instruction in enumerate(instructions[:5], 1):  # Show first 5
                            print(f"         {i}. {instruction}")
                        if len(instructions) > 5:
                            print(f"         ... and {len(instructions) - 5} more steps")
                    
                    # Show errors if any
                    errors = model_status.get("errors", [])
                    if errors:
                        print(f"      [ERROR] Errors:")
                        for error in errors:
                            print(f"         - {error}")
                
            except Exception as e:
                print(f"      [ERROR] Error: {e}")
        
        # Test router's model management
        print(f"\n[INFO] Testing Router Model Management...")
        print("=" * 60)
        
        # Test ensure_model without specifying backend
        print("[INFO] Testing router.ensure_model() with current backend:")
        
        current_backend = router.current_backend
        if current_backend:
            try:
                model_status = router.ensure_model("mistral")
                print(f"   Current backend: {current_backend}")
                print(f"   Model 'mistral' status: {'[OK] Available' if model_status.get('success') else '[WARN]️ Not available'}")
            except Exception as e:
                print(f"   [ERROR] Error: {e}")
        else:
            print("   [WARN]️  No current backend available")
        
        # Get available models for all backends
        print(f"\n[INFO] Available Models Summary:")
        available_models = router.get_available_models()
        
        for backend, models in available_models.items():
            if models:
                print(f"   🤖 {backend.upper()}: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}")
            else:
                print(f"   🤖 {backend.upper()}: No models available")
        
        # Save detailed report
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(reports_dir, f"model_management_test_{timestamp}.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed report saved to: {report_path}")
        
        # Final summary
        print(f"\n[INFO] Model Management Test completed!")
        print(f"[REPORT] Tested {total_backends} backends")
        print(f"[INFO] Tested {total_models} models per backend")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        for backend, backend_results in results["backends"].items():
            summary = backend_results["summary"]
            if summary["success_rate"] < 50:
                print(f"   [WARN]️  {backend.upper()}: Consider downloading more models")
            elif summary["success_rate"] >= 80:
                print(f"   [OK] {backend.upper()}: Well configured with good model coverage")
            else:
                print(f"   [REPORT] {backend.upper()}: Moderate model coverage")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies: pip install requests pyyaml")
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run() 