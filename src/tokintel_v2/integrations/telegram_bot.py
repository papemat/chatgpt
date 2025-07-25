import requests
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

def load_telegram_config(config_path: str = "config.yaml"):
    """Carica API key e chat id da config.yaml"""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    api_key = str(config.get('TELEGRAM_API_KEY')) if config.get('TELEGRAM_API_KEY') is not None else None
    chat_id = str(config.get('CHAT_ID')) if config.get('CHAT_ID') is not None else None
    if not api_key or not chat_id:
        raise ValueError("TELEGRAM_API_KEY o CHAT_ID mancante in config.yaml")
    return api_key, chat_id

def send_video_report(data: dict, config_path: str = "config.yaml") -> bool:
    """
    Invia un report video su Telegram.
    Args:
        data: dict con chiavi 'title', 'score', 'summary', 'suggestion'
        config_path: path al file di configurazione
    Returns:
        True se il messaggio è stato inviato con successo, False altrimenti
    """
    try:
        api_key, chat_id = load_telegram_config(config_path)
        url = f"https://api.telegram.org/bot{api_key}/sendMessage"
        message = (
            f"\U0001F4FA <b>{data.get('title', 'Video')}</b>\n"
            f"\u2B50 Punteggio engagement: <b>{data.get('score', '-')}</b>\n"
            f"\U0001F4DD Sintesi: {data.get('summary', '-')[:300]}\n"
            f"\U0001F4A1 Suggerimento: <i>{data.get('suggestion', '-')}</i>"
        )
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        resp = requests.post(url, data=payload, timeout=10)
        if resp.status_code == 200:
            logger.info("Messaggio Telegram inviato con successo")
            return True
        else:
            logger.error(f"Errore invio Telegram: {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        logger.error(f"Errore invio Telegram: {e}")
        return False 