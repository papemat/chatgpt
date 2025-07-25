import os
import sys
import json
from datetime import datetime

def run():
    print("🎤 Testing Whisper Integration...")
    
    # Aggiungi il path di TokIntel (path assoluto)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Risali di due livelli: tasks -> devika_tokintel -> Desktop
    desktop_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    tokintel_path = os.path.join(desktop_path, "TokIntel_v2")
    if tokintel_path not in sys.path:
        sys.path.insert(0, tokintel_path)
    
    # Non cambiare directory, solo aggiungere al path
    print(f"[INFO] TokIntel path: {tokintel_path}")
    
    try:
        # Test import
        print("[INFO] Testing imports...")
        from audio.whisper_transcriber import create_transcriber
        
        # Test configuration
        config = {
            'use_local': True,
            'use_api': False,
            'model_size': 'base',
            'device': 'auto',
            'batch_size': 16
        }
        
        print("[INFO] Creating transcriber...")
        transcriber = create_transcriber(config)
        
        # Test status
        print("[REPORT] Checking status...")
        status = transcriber.get_status()
        
        print(f"  Local available: {status['local_available']}")
        print(f"  API available: {status['api_available']}")
        print(f"  Model size: {status['model_size']}")
        print(f"  Device: {status['device']}")
        print(f"  Whisper installed: {status['whisper_installed']}")
        print(f"  OpenAI installed: {status['openai_installed']}")
        
        # Test with sample audio (if available)
        demo_dir = os.path.join(tokintel_path, "demo_input")
        if os.path.exists(demo_dir):
            print(f"\n🎵 Looking for demo files in {demo_dir}")
            
            audio_files = []
            for file in os.listdir(demo_dir):
                if file.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
                    audio_files.append(os.path.join(demo_dir, file))
            
            video_files = []
            for file in os.listdir(demo_dir):
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_files.append(os.path.join(demo_dir, file))
            
            if audio_files or video_files:
                print(f"  Found {len(audio_files)} audio files and {len(video_files)} video files")
                
                # Test with first audio file
                if audio_files:
                    test_file = audio_files[0]
                    print(f"\n🎤 Testing transcription with: {os.path.basename(test_file)}")
                    
                    try:
                        result = transcriber.transcribe(test_file)
                        print(f"  [OK] Transcription successful!")
                        print(f"  Text: {result['text'][:100]}...")
                        print(f"  Language: {result['language']}")
                        print(f"  Processing time: {result['processing_time']:.2f}s")
                        print(f"  Method: {result['method']}")
                        
                        # Save result
                        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
                        os.makedirs(reports_dir, exist_ok=True)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        report_path = os.path.join(reports_dir, f"whisper_test_{timestamp}.json")
                        
                        with open(report_path, 'w') as f:
                            json.dump(result, f, indent=2)
                        
                        print(f"  [INFO] Result saved: {report_path}")
                        
                    except Exception as e:
                        print(f"  [ERROR] Transcription failed: {e}")
                
                # Test with first video file
                if video_files:
                    test_file = video_files[0]
                    print(f"\n🎬 Testing video transcription with: {os.path.basename(test_file)}")
                    
                    try:
                        result = transcriber.transcribe(test_file)
                        print(f"  [OK] Video transcription successful!")
                        print(f"  Text: {result['text'][:100]}...")
                        print(f"  Language: {result['language']}")
                        print(f"  Processing time: {result['processing_time']:.2f}s")
                        print(f"  Method: {result['method']}")
                        
                    except Exception as e:
                        print(f"  [ERROR] Video transcription failed: {e}")
            else:
                print("  No audio/video files found for testing")
        else:
            print(f"  Demo directory not found: {demo_dir}")
        
        # Test batch processing
        print(f"\n[INFO] Testing batch processing...")
        test_files = []
        if audio_files:
            test_files.extend(audio_files[:2])  # First 2 audio files
        if video_files:
            test_files.extend(video_files[:1])  # First video file
        
        if test_files:
            try:
                results = transcriber.batch_transcribe(test_files)
                print(f"  [OK] Batch processing completed!")
                print(f"  Processed {len(results)} files")
                
                successful = sum(1 for r in results if 'error' not in r)
                print(f"  Successful: {successful}/{len(results)}")
                
            except Exception as e:
                print(f"  [ERROR] Batch processing failed: {e}")
        
        print(f"\n[INFO] Whisper integration test completed!")
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("💡 Install required dependencies:")
        print("  pip install openai-whisper")
        print("  pip install openai")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    run() 