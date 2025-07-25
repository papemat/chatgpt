import subprocess
import yaml
import time
import os
import requests
from pathlib import Path
from datetime import datetime

# Configurazione LM Studio
LM_API_URL = "http://localhost:1234/v1/chat/completions"
LM_MODEL = "gpt-4"  # puoi scrivere "codellama", "deepseek-coder", "phi", ecc.

LOG_FILE = "multi_step_agent_lmstudio.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def ai_refactor(file_path, instruction):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt = f"""Sei un esperto sviluppatore Python. Esegui questa istruzione:\n{instruction}\n\n---\n{content}"""

    payload = {
        "model": LM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2048,
        "stream": False
    }

    try:
        response = requests.post(LM_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()

        # Salvataggio backup + nuovo file
        backup_path = str(file_path) + ".bak"
        os.rename(file_path, backup_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)

        log(f"🧠 AI LM Studio ha aggiornato: {file_path} (backup: {backup_path})")
    except Exception as e:
        log(f"❌ Errore con LM Studio su {file_path}: {e}")

def run_command(command):
    log(f"▶️  {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        log(f"❌ Errore nel task: {command}")
    else:
        log(f"✅ Successo: {command}")

def main():
    if not os.path.exists("roadmap.yaml"):
        log("❌ File roadmap.yaml non trovato!")
        return
    with open("roadmap.yaml", "r", encoding="utf-8") as f:
        roadmap = yaml.safe_load(f)

    for task in roadmap.get("tasks", []):
        log(f"\n🔧 TASK: {task.get('name', 'Unnamed')}")

        if task.get("type") == "run":
            run_command(task["command"])

        elif task.get("type") == "ai":
            ai_refactor(Path(task["file"]), task["instruction"])

        time.sleep(1)

if __name__ == "__main__":
    main() 