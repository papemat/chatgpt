import json
from datetime import datetime
from pathlib import Path
import sys

# Permetti di passare input/output come argomenti
if len(sys.argv) > 1:
    INPUT_JSON = sys.argv[1]
else:
    INPUT_JSON = "audit_report_ui.json"

if len(sys.argv) > 2:
    OUTPUT_MD = sys.argv[2]
else:
    OUTPUT_MD = "AUDIT_REPORT_v2.2.md"


def file_section(file_info):
    md = f"## [FILE] {file_info['filename']}\n\n"
    if 'structure' in file_info:
        md += f"### [OK] Struttura e Obiettivo\n{file_info['structure']}\n\n"
    if 'typing' in file_info or 'docstring' in file_info or 'imports' in file_info or 'components' in file_info:
        md += "### [TECH] Analisi Tecnica\n"
        if 'typing' in file_info:
            md += f"- Typing: {file_info['typing']}\n"
        if 'docstring' in file_info:
            md += f"- Docstring: {file_info['docstring']}\n"
        if 'imports' in file_info:
            md += f"- Import: {file_info['imports']}\n"
        if 'components' in file_info:
            md += f"- Componenti: {file_info['components']}\n"
        md += "\n"
    if file_info.get('problems'):
        md += "### [WARN] Problemi rilevati\n"
        for p in file_info['problems']:
            md += f"- {p}\n"
        md += "\n"
    if file_info.get('suggestions'):
        md += "### [SUGGEST] Suggerimenti di Refactor\n"
        for s in file_info['suggestions']:
            md += f"- {s}\n"
        md += "\n"
    if 'status' in file_info:
        md += f"**Stato:** {file_info['status']}\n\n"
    return md


def main():
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    module = data.get("module", "")
    md = f"# [OK] TokIntel v2.2 – Audit Report (Modulo `{module}`)\n\n_Audit eseguito il: {today}_\n\n---\n\n"

    for file_info in data.get("files", []):
        md += file_section(file_info)
        md += "---\n\n"

    if data.get("global_suggestions"):
        md += "## [IDEAS] Suggerimenti Trasversali\n\n"
        for s in data["global_suggestions"]:
            md += f"- {s}\n"
        md += "\n"

    # Scrivi il file Markdown
    out_path = Path(OUTPUT_MD)
    out_path.write_text(md, encoding="utf-8")
    print(f"Report Markdown generato in: {out_path.resolve()}")

if __name__ == "__main__":
    main() 