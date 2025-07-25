#!/usr/bin/env python3
"""
Benchmark task for comparing different LLM backends
Enhanced with automatic model management
"""
import os
import sys
import json
import time
from datetime import datetime

def run():
    print("⚡ LLM Backend Benchmark Comparison (Enhanced)...")
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
        
        # Check status
        status = router.get_status()
        print(f"[REPORT] Router Status:")
        print(f"   Current Backend: {status.get('current_backend', 'None')}")
        print(f"   Available Backends: {status.get('available_backends', [])}")
        
        backend_status = status.get('backend_status', {})
        for backend, info in backend_status.items():
            available = info.get('available', False)
            models = info.get('models', [])
            print(f"   {backend}: {'[OK] Available' if available else '[ERROR] Unavailable'}")
            if models:
                print(f"     Models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
        
        # Test prompts
        test_prompts = [
            "Explain quantum computing in simple terms.",
            "Write a short poem about artificial intelligence.",
            "What are the benefits of renewable energy?",
            "How does machine learning work?",
            "Describe the future of technology."
        ]
        
        print(f"\n[INFO] Running benchmark with {len(test_prompts)} prompts...")
        
        # Define models for each backend
        models_config = {
            "lmstudio": "mistral",
            "ollama": "mistral"
        }
        
        # Run benchmark
        benchmark_results = router.benchmark_all(test_prompts, models_config)
        
        # Display results
        print("\n[REPORT] Benchmark Results:")
        print("=" * 60)
        
        backends_results = benchmark_results.get('backends', {})
        for backend, result in backends_results.items():
            if 'error' in result:
                print(f"[ERROR] {backend.upper()}: {result['error']}")
                continue
            
            successful = result.get('successful_requests', 0)
            total = result.get('total_prompts', 0)
            avg_time = result.get('average_time', 0)
            success_rate = (successful / total * 100) if total > 0 else 0
            
            print(f"[OK] {backend.upper()}:")
            print(f"   Success Rate: {success_rate:.1f}% ({successful}/{total})")
            print(f"   Average Time: {avg_time:.2f}s")
            print(f"   Total Time: {result.get('total_time', 0):.2f}s")
        
        # Display comparison
        comparison = benchmark_results.get('comparison', {})
        if comparison:
            print(f"\n🏆 Performance Comparison:")
            print("=" * 60)
            
            fastest = comparison.get('fastest_backend')
            most_reliable = comparison.get('most_reliable_backend')
            best_overall = comparison.get('best_overall')
            
            if fastest:
                print(f"⚡ Fastest: {fastest.upper()}")
            if most_reliable:
                print(f"🛡️  Most Reliable: {most_reliable.upper()}")
            if best_overall:
                print(f"🎯 Best Overall: {best_overall.upper()}")
            
            # Performance summary
            performance = comparison.get('performance_summary', {})
            if performance:
                print(f"\n[REPORT] Detailed Performance:")
                for backend, perf in performance.items():
                    success_rate = perf.get('success_rate', 0)
                    avg_time = perf.get('average_time', 0)
                    print(f"   {backend.upper()}: {success_rate:.1f}% success, {avg_time:.2f}s avg")
        
        # Test model management
        print(f"\n[INFO] Testing Model Management...")
        print("=" * 60)
        
        for backend in router.clients.keys():
            print(f"\n[INFO] Testing {backend.upper()} model management:")
            
            # Test ensure_model
            model_status = router.ensure_model("mistral", backend)
            if model_status.get("success"):
                print(f"   [OK] Model 'mistral' available in {backend}")
            else:
                print(f"   [WARN]️  Model 'mistral' not available in {backend}")
                if model_status.get("instructions"):
                    print(f"   [INFO] Instructions:")
                    for instruction in model_status["instructions"][:2]:  # Show first 2 instructions
                        print(f"      {instruction}")
        
        # Save detailed report
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        benchmark_path = os.path.join(reports_dir, f"benchmark_results_{timestamp}.json")
        
        with open(benchmark_path, 'w', encoding='utf-8') as f:
            json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed report saved to: {benchmark_path}")
        
        # Summary
        print(f"\n[INFO] Benchmark completed successfully!")
        print(f"[REPORT] Tested {len(backends_results)} backends")
        print(f"[INFO] Processed {len(test_prompts)} prompts")
        
        if comparison.get('best_overall'):
            print(f"🏆 Recommended backend: {comparison['best_overall'].upper()}")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies: pip install requests pyyaml")
    except Exception as e:
        print(f"[ERROR] Benchmark failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run() 