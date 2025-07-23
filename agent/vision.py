
import pytesseract
import cv2

class VisionAgent:
    @staticmethod
    def extract_text(frames):
        texts = []
        for idx, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            if text.strip():
                texts.append(text.strip())
        return "\n".join(texts)
