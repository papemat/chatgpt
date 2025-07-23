
import cv2
import os

class ScraperAgent:
    @staticmethod
    def extract_frames(video_path, every_n_frames=30):
        cap = cv2.VideoCapture(video_path)
        frames = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % every_n_frames == 0:
                frames.append(frame)
            count += 1
        cap.release()
        return frames
