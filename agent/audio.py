
import subprocess
import os

class AudioAgent:
    @staticmethod
    def transcribe(video_path):
        audio_path = video_path.replace(".mp4", ".wav")
        # Estrai audio dal video
        subprocess.call(['ffmpeg', '-i', video_path, '-ar', '16000', '-ac', '1', audio_path, '-y'])

        # Usa Whisper local (via subprocess o libreria)
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, language="it")
            return result['text']
        except Exception as e:
            return f"[Errore Whisper] {e}"
