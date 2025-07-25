#!/usr/bin/env python3
"""
Streamlit Launcher per TokIntel v2
Lancia l'interfaccia web di TokIntel v2 su porta 8502+ in modalità headless
"""

import os, sys, subprocess, time, webbrowser, socket
# Doppio controllo compatibilità
try:
    subprocess.run(["streamlit", "--version"], capture_output=True, check=True)
except Exception:
    subprocess.run([sys.executable, "-m", "streamlit", "--version"], capture_output=True, check=True)
# Cerca porta libera
base_port = 8502
for i in range(5):
    port = base_port + i
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) != 0:
            break
url = f"http://localhost:{port}"
with open(".tokintel_last_port", "w") as f:
    f.write(str(port))
print(f"[OK] Avvio TokIntel UI su {url}")
cmd = [sys.executable, "-m", "streamlit", "run", "tokintel/ui/streamlit_app.py", "--server.port", str(port)]
process = subprocess.Popen(cmd)
time.sleep(3)
webbrowser.open(url)
process.wait() 