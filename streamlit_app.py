
import streamlit as st
import os
from agent.scraper import ScraperAgent
from agent.vision import VisionAgent
from agent.audio import AudioAgent
from agent.synthesis import SynthesisAgent
from agent.scoring import ScoringAgent
from agent.exporter import ExporterAgent
from config import load_config

st.set_page_config(page_title="TokIntel v2", layout="wide")
st.title("📊 TokIntel v2 – Analisi Video TikTok")

uploaded_file = st.file_uploader("Carica un video TikTok (.mp4)", type=["mp4"])
config = load_config("config.yaml")

if uploaded_file:
    video_path = f"temp/{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(video_path)
    st.write("🔍 Estrazione frame e testi in corso...")

    frames = ScraperAgent.extract_frames(video_path)
    ocr_text = VisionAgent.extract_text(frames)
    transcript = AudioAgent.transcribe(video_path)
    summary = SynthesisAgent.summarize(transcript, ocr_text, config)
    score = ScoringAgent.evaluate(summary, transcript, ocr_text, config)

    ExporterAgent.export(video_path, summary, score, config)

    st.subheader("📝 Sintesi")
    st.json(summary)

    st.subheader("📈 Punteggio")
    st.json(score)
