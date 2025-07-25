# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for Playwright, ffmpeg, etc.)
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers
RUN pip install --upgrade pip && pip install playwright && playwright install --with-deps chromium

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install .

# Expose Streamlit port
EXPOSE 8501

# Default command: start Streamlit UI (can be overridden)
CMD ["streamlit", "run", "ui/interface.py"] 