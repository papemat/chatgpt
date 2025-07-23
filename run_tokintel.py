
import os
import argparse

# Controllo librerie principali
try:
    import openai
    import whisper
    import pytesseract
    import streamlit
    import yaml
    import cv2
    import fpdf
except ImportError:
    print("❌ Requisiti mancanti. Esegui prima: pip install -r requirements.txt")
    exit(1)

from agent.scraper import ScraperAgent
from agent.vision import VisionAgent
from agent.audio import AudioAgent
from agent.synthesis import SynthesisAgent
from agent.scoring import ScoringAgent
from agent.exporter import ExporterAgent
from config import load_config

def process_video(video_path, config):
    print(f"▶️ Analizzo: {video_path}")
    frames = ScraperAgent.extract_frames(video_path)
    ocr_text = VisionAgent.extract_text(frames)
    transcript = AudioAgent.transcribe(video_path)
    summary = SynthesisAgent.summarize(transcript, ocr_text, config)
    score = ScoringAgent.evaluate(summary, transcript, ocr_text, config)
    ExporterAgent.export(video_path, summary, score, config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--input", default="demo_input/")
    args = parser.parse_args()

    config = load_config(args.config)
    videos = [f for f in os.listdir(args.input) if f.endswith(".mp4")]

    for video in videos:
        process_video(os.path.join(args.input, video), config)
