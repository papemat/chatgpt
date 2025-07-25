import argparse
import sys
import logging
from pathlib import Path

def cli():
    parser = argparse.ArgumentParser(
        prog="tokintel",
        description="TokIntel v2 - Analizzatore Video TikTok (CLI)",
        epilog="Esempio: tokintel analyze sample.mp4"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analizza un video TikTok")
    analyze_parser.add_argument("input", help="Percorso al file video da analizzare")

    # dashboard
    dashboard_parser = subparsers.add_parser("dashboard", help="Avvia la dashboard analytics")

    # ui
    ui_parser = subparsers.add_parser("ui", help="Avvia la UI Streamlit")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[tokintel] %(message)s")

    if args.command == "analyze":
        video_path = Path(args.input)
        if not video_path.exists():
            logging.error(f"File non trovato: {video_path}")
            sys.exit(1)
        logging.info(f"[PLACEHOLDER] Analisi video: {video_path}")
        print("Analisi completata (mock). Score: 87/100")
    elif args.command == "dashboard":
        logging.info("[PLACEHOLDER] Avvio dashboard analytics...")
        print("Dashboard avviata (mock). Apri http://localhost:8501")
    elif args.command == "ui":
        logging.info("[PLACEHOLDER] Avvio UI Streamlit...")
        print("UI Streamlit avviata (mock). Apri http://localhost:8501")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    cli() 