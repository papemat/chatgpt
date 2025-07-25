# DONE: Typing completo aggiunto
# DONE: Docstring Google-style aggiunte
# DONE: Logger strutturato implementato
# DONE: Try/except granulari implementati
# DONE: Validazione input aggiunta

# [REPORT] Analytics Dashboard - TokIntel v2
# Utility per salvataggio e query di statistiche analitiche su SQLite
"""
[REPORT] Analytics Dashboard - TokIntel v2
Utility per salvataggio e query di statistiche analitiche su SQLite
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configurazione logging
logger = logging.getLogger(__name__)

DB_PATH = Path("db/analytics.db")

# Assicura che la directory esista
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _init_db() -> None:
    """Inizializza il database SQLite per analytics"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_title TEXT,
                score REAL,
                sentiment REAL,
                keywords TEXT,
                summary TEXT,
                created_at TEXT
            )''')
            conn.commit()
            logger.info("Database analytics inizializzato con successo")
    except sqlite3.Error as e:
        logger.error(f"Errore nell'inizializzazione database analytics: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore generico nell'inizializzazione database: {e}")
        raise

_init_db()

def update_stats(result_json: Dict[str, Any]) -> bool:
    """
    Salva i risultati di analisi su SQLite.
    
    Args:
        result_json: Dizionario con i risultati dell'analisi
        
    Returns:
        True se il salvataggio è riuscito, False altrimenti
        
    Raises:
        ValueError: Se i dati di input non sono validi
        sqlite3.Error: Se c'è un errore del database
    """
    try:
        # Validazione input
        if not isinstance(result_json, dict):
            raise ValueError("result_json deve essere un dizionario")
        
        if 'video_title' not in result_json:
            raise ValueError("video_title è richiesto in result_json")
        
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO analytics (video_title, score, sentiment, keywords, summary, created_at)
                         VALUES (?, ?, ?, ?, ?, ?)''', (
                result_json.get('video_title', 'Video'),
                float(result_json.get('overall_score', 0)),
                float(result_json.get('sentiment', 0)),
                ','.join(result_json.get('keywords', [])),
                result_json.get('summary', ''),
                datetime.now().isoformat()
            ))
            conn.commit()
            logger.info(f"Statistiche aggiornate per video: {result_json.get('video_title', 'Video')}")
            return True
    except ValueError as e:
        logger.error(f"Errore di validazione input: {e}")
        raise
    except sqlite3.Error as e:
        logger.error(f"Errore database nel salvataggio statistiche: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore generico nel salvataggio statistiche: {e}")
        raise

def get_top_videos(limit: int = 10) -> List[Tuple[str, float, str]]:
    """
    Restituisce i video con punteggio più alto.
    
    Args:
        limit: Numero massimo di video da restituire (default: 10)
        
    Returns:
        Lista di tuple (video_title, score, created_at)
        
    Raises:
        ValueError: Se limit non è un intero positivo
        sqlite3.Error: Se c'è un errore del database
    """
    try:
        # Validazione input
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit deve essere un intero positivo")
        
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT video_title, score, created_at FROM analytics ORDER BY score DESC LIMIT ?''', (limit,))
            results = c.fetchall()
            logger.info(f"Recuperati {len(results)} video top")
            return results
    except ValueError as e:
        logger.error(f"Errore di validazione input: {e}")
        raise
    except sqlite3.Error as e:
        logger.error(f"Errore database nel recupero top video: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore generico nel recupero top video: {e}")
        raise

def get_sentiment_trend() -> List[Tuple[str, float]]:
    """
    Restituisce la lista (created_at, sentiment) per trend temporale.
    
    Returns:
        Lista di tuple (created_at, sentiment)
        
    Raises:
        sqlite3.Error: Se c'è un errore del database
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT created_at, sentiment FROM analytics ORDER BY created_at ASC''')
            results = c.fetchall()
            logger.info(f"Recuperati {len(results)} punti per trend sentiment")
            return results
    except sqlite3.Error as e:
        logger.error(f"Errore database nel recupero trend sentiment: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore generico nel recupero trend sentiment: {e}")
        raise

def get_keywords_cloud() -> List[str]:
    """
    Restituisce tutte le keywords per wordcloud.
    
    Returns:
        Lista di keywords
        
    Raises:
        sqlite3.Error: Se c'è un errore del database
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT keywords FROM analytics''')
            keywords = []
            for row in c.fetchall():
                keywords.extend(row[0].split(','))
            cleaned_keywords = [k.strip() for k in keywords if k.strip()]
            logger.info(f"Recuperate {len(cleaned_keywords)} keywords per wordcloud")
            return cleaned_keywords
    except sqlite3.Error as e:
        logger.error(f"Errore database nel recupero keywords: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore generico nel recupero keywords: {e}")
        raise 