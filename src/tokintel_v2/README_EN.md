[![CI](https://github.com/TUO_USERNAME/TUO_REPO/actions/workflows/tests.yml/badge.svg)](https://github.com/TUO_USERNAME/TUO_REPO/actions)
[![codecov](https://codecov.io/gh/TUO_USERNAME/TUO_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/TUO_USERNAME/TUO_REPO)
[![PyPI version](https://img.shields.io/pypi/v/tokintel.svg)](https://pypi.org/project/tokintel/)

# DONE: README.md updated with test/linting/refactor instructions

# 🎯 TokIntel v2 - TikTok Video Analyzer

[![PyPI - CLI Ready](https://img.shields.io/badge/CLI-tokintel-blue?logo=python&label=tokintel%20CLI)](https://pypi.org/project/tokintel/)
[![PyPI - pip install .](https://img.shields.io/badge/pip%20install-.--success?logo=pypi)](https://pypi.org/project/tokintel/)

**Modular TikTok video analyzer with scalable architecture and full automation.**

## [INFO] Main Features

- **[REPORT] Advanced Video Analysis**: Frame extraction, content analysis, performance metrics
- **🤖 AI Integration**: Integration with AI models for semantic analysis
- **💾 PostgreSQL Database**: Robust storage system with SQLAlchemy
- **🕷️ TikTok Scraping**: Automatic download of videos and metadata
- **⏰ Automatic Scheduler**: Scheduled batch analysis
- **[INFO] Streamlit UI**: Modern and intuitive web interface
- **[REPORT] Analytics Dashboard**: Trends, insights, and reporting
- **[INFO] Full Automation**: Automatic tests, linting, type checking

## [INFO] Installation

### Via pip
```bash
pip install tokintel
```

### Via pipx (recommended)
```bash
pipx install git+https://github.com/TUO_USERNAME/TUO_REPO.git
```
> [INFO] Make sure you have `pipx` installed and PATH configured

## [INFO] Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite for development)
- Playwright for scraping

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/your-org/tokintel-v2.git
cd tokintel-v2

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Base dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### Configuration

1. **Database**: Configure PostgreSQL or use SQLite for development
2. **Playwright**: Install browser for scraping
   ```bash
   playwright install chromium
   ```
3. **Configuration**: Copy and edit `config/config.yaml.example`

## [INFO] Testing and Code Quality

### Automated Tests

```bash
# Run all tests
python scripts/run_tests.py

# Unit tests only
python scripts/run_tests.py --unit-only

# Integration tests only
python scripts/run_tests.py --integration-only

# Tests with coverage
python scripts/run_tests.py --no-linting --no-type-checking
```

### Linting and Type Checking

```bash
# Code formatting
black .

# Import sorting
isort .

# Linting
flake8 .

# Type checking
mypy .

# All together
python scripts/run_tests.py --no-coverage
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## [INFO] Development

### Project Structure

```
TokIntel_v2/
├── [INFO] core/           # Core functionalities
├── [INFO] db/            # Database and models
├── [INFO] scraper/       # TikTok scraping
├── [INFO] analytics/     # Data analysis
├── [INFO] ui/            # Streamlit interfaces
├── [INFO] scheduler/     # Automatic scheduler
├── [INFO] scripts/       # Utility scripts
├── [INFO] tests/         # Unit and integration tests
├── [INFO] config/        # Configurations
└── [INFO] tools/         # Development tools
```

### Development Workflow

1. **Setup environment**:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

2. **Development**:
   ```bash
   # Code with automatic validation
   git add .
   git commit -m "feat: new feature"
   ```

3. **Testing**:
   ```bash
   # Full tests
   python scripts/run_tests.py
   
   # Coverage report
   open coverage_html/index.html
   ```

### Refactor and Utilities

```bash
# Generate refactor report
python scripts/refactor_utils.py --generate-report

# Update TODO
python scripts/refactor_utils.py --update-todo

# Scan # DONE: comments
python scripts/refactor_utils.py --scan-done

# Convert JSON to Markdown
python scripts/refactor_utils.py --json-to-md file.json
```

## [INFO] Usage

### CLI Installation

```bash
pip install .
```

### CLI Usage Example

```bash
# Analyze a video
$ tokintel analyze sample.mp4

# Start the dashboard
$ tokintel dashboard

# Start the Streamlit UI
$ tokintel ui

# Help
$ tokintel --help

# Fallback: run via module
$ python -m tokintel analyze sample.mp4
```

### Web Interface

```bash
# Start Streamlit
streamlit run ui/interface.py

# Pro Dashboard
streamlit run ui/pro_dashboard.py

# TikTok Library
streamlit run ui/tiktok_library.py
```

### CLI

```bash
# Single video analysis
python main.py --video path/to/video.mp4

# Automatic scheduler
python scheduler/auto_scheduler.py --user-id 1 --interval 60

# Batch analysis
python batch_auto_analyze.py --user-id 1
```

### API

```python
from core import TokIntelCore

# Initialize
core = TokIntelCore()

# Analyze video
results = await core.analyze_video("video.mp4")
print(f"Score: {results['overall_score']}")
```

## [REPORT] Dashboard and Analytics

### Main Metrics

- **Overall Score**: Overall video score
- **Engagement Rate**: Predicted engagement rate
- **Viral Potential**: Viral potential
- **Content Quality**: Content quality
- **Trend Analysis**: Temporal trend analysis

### Available Insights

- **Keywords**: Extracted keywords
- **Emotions**: Emotional analysis
- **Themes**: Content themes
- **Recommendations**: Improvement suggestions
- **Competitive Analysis**: Competitive analysis

## [INFO] Advanced Configuration

### Database

```yaml
# config/config.yaml
database:
  type: postgresql  # or sqlite
  host: localhost
  port: 5432
  name: tokintel
  user: postgres
  password: your_password
```

### AI Models

```yaml
ai:
  provider: openai  # or local
  model: gpt-4
  api_key: your_api_key
  temperature: 0.7
```

### Scheduler

```yaml
scheduler:
  enabled: true
  interval_minutes: 60
  max_concurrent_jobs: 5
  retry_attempts: 3
```

## [INFO] Testing

### Unit Tests

```bash
# Run specific tests
pytest tests/test_database.py -v

# Tests with coverage
pytest --cov=. --cov-report=html

# Parallel tests
pytest -n auto
```

### Integration Tests

```bash
# Database tests
pytest tests/test_database_integration.py

# Scraper tests
pytest tests/test_scraper_integration.py

# UI tests
pytest tests/test_ui_integration.py
```

### Performance Tests

```bash
# Profiling
python -m cProfile -o profile.stats main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

## [REPORT] Monitoring

### Logs

```bash
# System log
tail -f logs/tokintel.log

# Scheduler log
tail -f logs/scheduler.log

# Scraping log
tail -f logs/scraper.log
```

### Metrics

```python
from analytics.dashboard import get_analytics_summary

# General statistics
stats = get_analytics_summary(user_id=1, days=30)
print(f"Analyzed videos: {stats['total_analyses']}")
```

## [INFO] Security

### Best Practices

- [OK] Input validation in all modules
- [OK] Granular error handling
- [OK] Structured logging
- [OK] Full type checking
- [OK] Automatic linting
- [OK] Security testing with Bandit

### Security Configuration

```yaml
security:
  input_validation: true
  sql_injection_protection: true
  xss_protection: true
  rate_limiting: true
  max_file_size: 100MB
```

## 🤝 Contributing

### Development Setup

1. **Fork** the repository
2. **Clone** your fork
3. **Feature branch**: `git checkout -b feature/new-feature`
4. **Commit** with standard: `git commit -m "feat: description"`
5. **Push** and **Pull Request**

### Code Standards

- **Black** for formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **Google-style docstrings**
- **Tests** for all features

### PR Checklist

- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] Linting passes with flake8
- [ ] Type checking passes with mypy
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Documentation updated
- [ ] Pre-commit hooks pass

## [INFO] License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/tokintel-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/tokintel-v2/discussions)
- **Email**: team@tokintel.com

---

TokIntel v2.0.0 is public, stable, documented, and deployable anywhere.

## [INFO] Coverage

To enable the coverage badge, register the repo on https://codecov.io and add the `CODECOV_TOKEN` in GitHub Secrets.

## [INFO] Deploy & Distribution

- **PyPI:** Install with `pip install tokintel` ([PyPI](https://pypi.org/project/tokintel/))
- **Streamlit Live Demo:** [https://streamlit.io/cloud/demo-link](https://streamlit.io/cloud/demo-link) <!-- Replace with real link -->
- **Docker:** Start with `docker-compose up`
- **Colab:** [TokIntel_Colab_Demo_EN.ipynb](TokIntel_Colab_Demo_EN.ipynb)
- **HuggingFace Spaces:** (coming soon)

---

TokIntel v2.0.0 is public, stable, documented, and deployable anywhere.

## 🏷 Automatic Versioning

Easily manage versions and changelog:

```bash
# Show current version
python scripts/version.py --version

# Bump patch (e.g. 2.0.0 → 2.0.1)
python scripts/version.py --bump patch

# Bump minor (e.g. 2.0.1 → 2.1.0)
python scripts/version.py --bump minor

# Set a specific version
python scripts/version.py --set 2.2.0

# Bump and create git tag
python scripts/version.py --bump patch --tag
``` 