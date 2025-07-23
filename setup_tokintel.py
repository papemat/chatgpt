
import subprocess

REQUIRED_PACKAGES = [
    "openai",
    "whisper",
    "pytesseract",
    "streamlit",
    "pyyaml",
    "opencv-python",
    "fpdf"
]

for package in REQUIRED_PACKAGES:
    print(f"✅ Installo {package}...")
    subprocess.call(["pip", "install", package])
