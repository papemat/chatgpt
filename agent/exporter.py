
import os
import json
import csv

class ExporterAgent:
    @staticmethod
    def export(video_path, summary, score, config):
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_folder = config.get("output_folder", "output/")
        os.makedirs(output_folder, exist_ok=True)

        if "json" in config.get("export_format", []):
            with open(os.path.join(output_folder, f"{base_name}_summary.json"), "w") as f:
                json.dump({"summary": summary, "score": score}, f, indent=2)

        if "csv" in config.get("export_format", []):
            csv_path = os.path.join(output_folder, f"{base_name}_summary.csv")
            with open(csv_path, "w", newline='') as csvfile:
                fieldnames = ["video", "score", "matched_keywords", "ocr_detected", "speech_density"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    "video": base_name,
                    "score": score["score"],
                    "matched_keywords": ",".join(score["matched_keywords"]),
                    "ocr_detected": score["ocr_detected"],
                    "speech_density": score["speech_density"]
                })
