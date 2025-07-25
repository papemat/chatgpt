import argparse
import re
import sys
from datetime import date
from pathlib import Path
import subprocess

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"
CHANGELOG = Path(__file__).parent.parent / "CHANGELOG.md"

SEMVER_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')


def get_current_version():
    content = PYPROJECT.read_text(encoding="utf-8")
    m = re.search(r"version\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", content)
    if not m:
        print("Version not found in pyproject.toml", file=sys.stderr)
        sys.exit(1)
    return m.group(1)


def bump_version(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        return f"{major+1}.0.0"
    elif part == "minor":
        return f"{major}.{minor+1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch+1}"
    else:
        raise ValueError("part must be one of: major, minor, patch")


def set_version(new_version):
    content = PYPROJECT.read_text(encoding="utf-8")
    new_content = re.sub(r'(version\s*=\s*["\"]).*?(["\"])', f'\\1{new_version}\\2', content)
    PYPROJECT.write_text(new_content, encoding="utf-8")
    print(f"pyproject.toml aggiornato a {new_version}")


def update_changelog(new_version):
    today = date.today().isoformat()
    content = CHANGELOG.read_text(encoding="utf-8")
    unreleased = re.search(r'## \[Unreleased\](.*?)(?=^## |\Z)', content, re.DOTALL | re.MULTILINE)
    if not unreleased:
        print("Sezione [Unreleased] non trovata in CHANGELOG.md", file=sys.stderr)
        sys.exit(1)
    unreleased_content = unreleased.group(1).strip()
    if not unreleased_content:
        unreleased_content = "- Aggiornamento versione."
    new_section = f"## [{new_version}] - {today}\n{unreleased_content}\n\n## [Unreleased]\n"
    # Sostituisci la sezione Unreleased
    new_content = re.sub(r'## \[Unreleased\](.*?)(?=^## |\Z)', new_section, content, flags=re.DOTALL | re.MULTILINE)
    CHANGELOG.write_text(new_content, encoding="utf-8")
    print(f"CHANGELOG.md aggiornato con la sezione {new_version}")


def git_commit_and_tag(new_version, do_tag):
    subprocess.run(["git", "add", str(PYPROJECT), str(CHANGELOG)], check=True)
    subprocess.run(["git", "commit", "-m", f"chore(release): v{new_version}"], check=True)
    if do_tag:
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        print(f"Tag v{new_version} creato.")
        if input("Vuoi pushare il tag su origin? [y/N] ").lower() == "y":
            subprocess.run(["git", "push", "origin", f"v{new_version}"], check=True)


def main():
    parser = argparse.ArgumentParser(description="Gestione versioni TokIntel v2")
    parser.add_argument("--version", action="store_true", help="Mostra la versione attuale")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Incrementa la versione")
    parser.add_argument("--set", metavar="X.Y.Z", help="Imposta una versione specifica")
    parser.add_argument("--tag", action="store_true", help="Crea anche un tag git dopo il bump")
    args = parser.parse_args()

    current = get_current_version()
    print(f"Versione attuale: {current}")

    if args.version and not (args.bump or args.set):
        sys.exit(0)

    if args.bump:
        new_version = bump_version(current, args.bump)
    elif args.set:
        if not SEMVER_RE.match(args.set):
            print("Versione non valida. Usa formato X.Y.Z", file=sys.stderr)
            sys.exit(1)
        new_version = args.set
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Nuova versione: {new_version}")
    set_version(new_version)
    update_changelog(new_version)
    git_commit_and_tag(new_version, args.tag)

if __name__ == "__main__":
    main() 