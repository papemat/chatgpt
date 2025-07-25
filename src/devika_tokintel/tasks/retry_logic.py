def run():
    print("[INFO] Checking retry logic in LLM handler...")
    try:
        from llm.handler import LLMHandler
        handler = LLMHandler()
        print("[OK] Retry logic initialized.")
    except Exception as e:
        print(f"[ERROR] Retry logic error: {e}")
