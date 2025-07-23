
from openai import OpenAI

class SynthesisAgent:
    @staticmethod
    def summarize(transcript, ocr_text, config):
        prompt = f"""Analizza il seguente contenuto:
- Trascrizione audio: {transcript}
- Testo OCR rilevato: {ocr_text}

Restituisci una sintesi breve del contenuto del video in italiano, elencando il tema principale, eventuali emozioni trasmesse e se è presente un 'hook' iniziale forte."""
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=config.get("model", "gpt-4"),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Errore durante la sintesi] {e}"
