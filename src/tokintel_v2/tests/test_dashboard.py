import pytest
import os
import tempfile
import shutil
from analytics import dashboard
from pathlib import Path
import sqlite3

def setup_temp_db(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / 'analytics.db'
    monkeypatch.setattr(dashboard, 'DB_PATH', db_path)
    dashboard._init_db()
    return db_path, temp_dir

def teardown_temp_db(temp_dir):
    shutil.rmtree(temp_dir)

def test_update_and_query(monkeypatch):
    db_path, temp_dir = setup_temp_db(monkeypatch)
    try:
        # Inserisci dati
        dashboard.update_stats({
            'video_title': 'Test Video',
            'overall_score': 0.9,
            'sentiment': 0.7,
            'keywords': ['viral', 'trend'],
            'summary': 'Sintesi test'
        })
        dashboard.update_stats({
            'video_title': 'Altro Video',
            'overall_score': 0.5,
            'sentiment': 0.2,
            'keywords': ['marketing'],
            'summary': 'Altro'
        })
        # Test get_top_videos
        top = dashboard.get_top_videos()
        assert len(top) == 2
        assert top[0][0] == 'Test Video'
        # Test get_sentiment_trend
        trend = dashboard.get_sentiment_trend()
        assert len(trend) == 2
        assert trend[0][1] == 0.7
        # Test get_keywords_cloud
        cloud = dashboard.get_keywords_cloud()
        assert 'viral' in cloud
        assert 'marketing' in cloud
    finally:
        import sqlite3, gc
        sqlite3.connect(db_path).close()
        gc.collect()
        teardown_temp_db(temp_dir) 