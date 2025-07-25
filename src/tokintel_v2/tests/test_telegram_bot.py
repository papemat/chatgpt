import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent))
from integrations import telegram_bot

def test_load_telegram_config(tmp_path):
    # Crea un file di config temporaneo
    config = {'TELEGRAM_API_KEY': 'testkey', 'CHAT_ID': '12345'}
    config_file = tmp_path / 'config.yaml'
    config_file.write_text('TELEGRAM_API_KEY: testkey\nCHAT_ID: 12345\n', encoding='utf-8')
    api_key, chat_id = telegram_bot.load_telegram_config(str(config_file))
    assert api_key == 'testkey'
    assert chat_id == '12345'

@patch('integrations.telegram_bot.requests.post')
def test_send_video_report_success(mock_post, tmp_path):
    # Mock config
    config = {'TELEGRAM_API_KEY': 'testkey', 'CHAT_ID': '12345'}
    config_file = tmp_path / 'config.yaml'
    config_file.write_text('TELEGRAM_API_KEY: testkey\nCHAT_ID: 12345\n', encoding='utf-8')
    # Mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_post.return_value = mock_resp
    data = {'title': 'Test', 'score': 9.5, 'summary': 'Sintesi', 'suggestion': 'Ottimizza'}
    assert telegram_bot.send_video_report(data, str(config_file)) is True

@patch('integrations.telegram_bot.requests.post')
def test_send_video_report_api_error(mock_post, tmp_path):
    config = {'TELEGRAM_API_KEY': 'testkey', 'CHAT_ID': '12345'}
    config_file = tmp_path / 'config.yaml'
    config_file.write_text('TELEGRAM_API_KEY: testkey\nCHAT_ID: 12345\n', encoding='utf-8')
    mock_resp = MagicMock()
    mock_resp.status_code = 400
    mock_resp.text = 'Bad Request'
    mock_post.return_value = mock_resp
    data = {'title': 'Test', 'score': 9.5, 'summary': 'Sintesi', 'suggestion': 'Ottimizza'}
    assert telegram_bot.send_video_report(data, str(config_file)) is False

def test_send_video_report_config_error(tmp_path):
    # Config mancante
    data = {'title': 'Test'}
    result = telegram_bot.send_video_report(data, str(tmp_path / 'missing.yaml'))
    assert result is False 