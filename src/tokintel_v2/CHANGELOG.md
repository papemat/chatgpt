# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [2.1.0] - 2025-07-25

### Added
- Modulo `extensions/export_tools.py` per esportazione avanzata (CSV, PDF, Excel, ZIP)
- Test automatici (`tests/test_export_tools.py`) con `pytest` (8 test passati)
- Integrazione completa nella UI Streamlit (4 bottoni di esportazione)
- Funzioni `export_to_csv()`, `export_to_pdf()`, `export_to_excel()`, `export_to_zip()`
- Download diretto dei file esportati dall'interfaccia web
- Dipendenze `reportlab` (PDF) e `openpyxl` (Excel)
- Export ZIP con metadati, README e file multipli
- Formattazione Excel con header colorati e auto-adjust colonne

### Changed
- Aggiornato README.md con sezione esportazione dati completa
- Migliorata gestione errori nella UI Streamlit
- UI espansa da 2 a 4 colonne per i bottoni di esportazione

## [2.0.0] - 2025-07-24
### Added
- Logging avanzato e rotazione log via RotatingFileHandler.
- Test edge-case per scraping (video non trovato, timeout Playwright) e scoring (input vuoto, rumore, categorie ignote).
- Packaging CLI production-grade e supporto `pipx`.
- Automazione test, linting, type-checking (pytest, mypy, flake8, black).
- CI/CD GitHub Actions con badge e upload coverage.
- Refactor, modularizzazione e typing completo dei moduli chiave. 