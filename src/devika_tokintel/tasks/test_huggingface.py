import os
import sys
import json
from datetime import datetime

def run():
    print("🤗 Testing HuggingFace Integration...")
    
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
        from huggingface.inference import create_hf_inference
        
        # Test configuration
        config = {
            'device': 'auto',
            'use_gpu': True,
            'max_length': 512,
            'batch_size': 1,
            'models': {
                'summarization': 'facebook/bart-large-cnn',
                'sentiment': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                'ner': 'dbmdz/bert-large-cased-finetuned-conll03-english'
            }
        }
        
        print("[INFO] Creating HuggingFace inference engine...")
        hf = create_hf_inference(config)
        
        # Test status
        print("[REPORT] Checking status...")
        status = hf.get_status()
        
        print(f"  HF available: {status['hf_available']}")
        print(f"  NumPy available: {status['numpy_available']}")
        print(f"  Device: {status['device']}")
        print(f"  Use GPU: {status['use_gpu']}")
        print(f"  Available pipelines: {', '.join(status['available_pipelines'])}")
        print(f"  Max length: {status['max_length']}")
        print(f"  Batch size: {status['batch_size']}")
        
        if not status['hf_available']:
            print("[ERROR] HuggingFace Transformers not available")
            print("💡 Install required dependencies:")
            print("  pip install transformers torch")
            return
        
        # Test texts
        test_texts = [
            "Artificial intelligence is transforming the world. Machine learning algorithms are becoming more sophisticated and capable of solving complex problems. Companies are investing heavily in AI research and development.",
            "I love this new product! It's amazing and works perfectly. The customer service was also excellent.",
            "The weather is terrible today. I'm feeling really disappointed about the rain."
        ]
        
        # Test summarization
        print(f"\n[INFO] Testing summarization...")
        test_text = test_texts[0]
        
        try:
            result = hf.summarize(test_text, max_length=100, min_length=30)
            print(f"  [OK] Summarization successful!")
            print(f"  Original: {test_text[:100]}...")
            print(f"  Summary: {result['summary']}")
            print(f"  Processing time: {result['processing_time']:.2f}s")
            
            # Save result
            reports_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(reports_dir, f"hf_summarization_{timestamp}.json")
            
            with open(report_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"  [INFO] Result saved: {report_path}")
            
        except Exception as e:
            print(f"  [ERROR] Summarization failed: {e}")
        
        # Test sentiment analysis
        print(f"\n😊 Testing sentiment analysis...")
        
        for i, text in enumerate(test_texts):
            try:
                result = hf.analyze_sentiment(text)
                print(f"  Text {i+1}: {text[:50]}...")
                print(f"    Sentiment: {result['top_prediction']['label']}")
                print(f"    Score: {result['top_prediction']['score']:.3f}")
                
            except Exception as e:
                print(f"  [ERROR] Sentiment analysis failed for text {i+1}: {e}")
        
        # Test NER (Named Entity Recognition)
        print(f"\n🏷️ Testing Named Entity Recognition...")
        ner_text = "Apple Inc. CEO Tim Cook announced new products at the WWDC conference in San Francisco."
        
        try:
            result = hf.extract_entities(ner_text)
            print(f"  [OK] NER successful!")
            print(f"  Text: {ner_text}")
            print(f"  Entities found:")
            
            for entity_type, entities in result['entities'].items():
                print(f"    {entity_type}: {[e['text'] for e in entities]}")
            
            print(f"  Processing time: {result['processing_time']:.2f}s")
            
        except Exception as e:
            print(f"  [ERROR] NER failed: {e}")
        
        # Test keyword extraction
        print(f"\n[INFO] Testing keyword extraction...")
        
        try:
            result = hf.extract_keywords(test_texts[0], top_k=5)
            print(f"  [OK] Keyword extraction successful!")
            print(f"  Keywords:")
            
            for keyword in result['keywords']:
                print(f"    {keyword['text']} ({keyword['type']}) - Score: {keyword['score']:.3f}")
            
        except Exception as e:
            print(f"  [ERROR] Keyword extraction failed: {e}")
        
        # Test classification
        print(f"\n🏷️ Testing text classification...")
        
        try:
            result = hf.classify(test_texts[0], task='classification')
            print(f"  [OK] Classification successful!")
            print(f"  Top prediction: {result['top_prediction']['label']}")
            print(f"  Score: {result['top_prediction']['score']:.3f}")
            
        except Exception as e:
            print(f"  [ERROR] Classification failed: {e}")
        
        # Test batch processing
        print(f"\n[INFO] Testing batch processing...")
        
        try:
            results = hf.batch_process(test_texts, task='sentiment')
            print(f"  [OK] Batch processing completed!")
            print(f"  Processed {len(results)} texts")
            
            successful = sum(1 for r in results if 'error' not in r)
            print(f"  Successful: {successful}/{len(results)}")
            
            for i, result in enumerate(results):
                if 'error' not in result:
                    sentiment = result['top_prediction']['label']
                    score = result['top_prediction']['score']
                    print(f"    Text {i+1}: {sentiment} ({score:.3f})")
                else:
                    print(f"    Text {i+1}: Error - {result['error']}")
            
        except Exception as e:
            print(f"  [ERROR] Batch processing failed: {e}")
        
        # Test benchmark
        print(f"\n⚡ Testing benchmark...")
        
        try:
            benchmark = hf.benchmark_pipeline('sentiment', test_texts)
            print(f"  [OK] Benchmark completed!")
            print(f"  Task: {benchmark['task']}")
            print(f"  Test texts: {benchmark['test_texts']}")
            print(f"  Successful tests: {benchmark['successful_tests']}")
            print(f"  Total time: {benchmark['total_time']:.2f}s")
            print(f"  Average time: {benchmark['average_time']:.2f}s")
            
            # Save benchmark
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            reports_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
            os.makedirs(reports_dir, exist_ok=True)
            benchmark_path = os.path.join(reports_dir, f"hf_benchmark_{timestamp}.json")
            
            with open(benchmark_path, 'w') as f:
                json.dump(benchmark, f, indent=2)
            
            print(f"  [INFO] Benchmark saved: {benchmark_path}")
            
        except Exception as e:
            print(f"  [ERROR] Benchmark failed: {e}")
        
        print(f"\n[INFO] HuggingFace integration test completed!")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies:")
        print("  pip install transformers torch numpy")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    run() 