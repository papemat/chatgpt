
class ScoringAgent:
    @staticmethod
    def evaluate(summary, transcript, ocr_text, config):
        score = 0
        matched = []

        for kw in config.get("keywords", []):
            if kw.lower() in summary.lower() or kw.lower() in transcript.lower():
                score += config["weights"].get("keywords", 1.0)
                matched.append(kw)

        if transcript:
            speech_density = len(transcript.split()) / 60  # parole al minuto (approssimato)
            score += speech_density * config["weights"].get("speech_density", 1.0)
        else:
            speech_density = 0

        if ocr_text.strip():
            score += config["weights"].get("ocr", 1.0)
            ocr_detected = True
        else:
            ocr_detected = False

        return {
            "score": round(score, 2),
            "matched_keywords": matched,
            "speech_density": round(speech_density, 2),
            "ocr_detected": ocr_detected
        }
