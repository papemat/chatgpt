def run():
    print("[OK] Running test: config validation")
    try:
        from core.config import ConfigManager
        config = ConfigManager("config/config.yaml")
        print("[OK] Config loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Config error: {e}")
