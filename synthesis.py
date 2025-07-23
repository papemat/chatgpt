import requests

class SynthesisAgent:
    @staticmethod
    def summarize(transcript, ocr_text, config):
        prompt = f"""
Analizza il seguente contenuto video TikTok:

- Trascrizione audio: {transcript}
- Testo visivo rilevato tramite OCR: {ocr_text}

Obiettivo:
1. Riassumi brevemente il contenuto in italiano
2. Indica il tema centrale del video
3. Specifica eventuali emozioni trasmesse
4. Valuta se è presente un 'hook' efficace nei primi secondi
"""

        try:
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "model": "local-model",  # oppure lascia vuoto se LM Studio non lo richiede
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30  # Aggiunto timeout per evitare blocchi infiniti
            )
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[Errore durante la sintesi con LM Studio] {e}"