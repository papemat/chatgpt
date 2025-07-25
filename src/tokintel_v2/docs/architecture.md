# TokIntel v2 – Architecture Overview

## Module Map

- **core/**: Core logic, scoring, orchestration
- **db/**: Database models and persistence
- **scraper/**: TikTok scraping and data extraction
- **analytics/**: Data analysis and reporting
- **ui/**: Streamlit web UI
- **scheduler/**: Batch and scheduled analysis
- **scripts/**: Utilities, versioning, publishing
- **tests/**: Unit and integration tests
- **config/**: Configuration files
- **tools/**: Developer tools

## Data Flow

1. **Video Input**: User uploads or specifies a TikTok video
2. **Scraping**: Video and metadata are scraped from TikTok
3. **Scoring**: Video is analyzed and scored by core logic
4. **Database**: Results are stored in db/
5. **UI/CLI**: Results are shown in Streamlit UI or via CLI

## Key Files

- [CHANGELOG.md](../CHANGELOG.md)
- [pyproject.toml](../pyproject.toml)

---

For more details, see the README or open an issue for support. 