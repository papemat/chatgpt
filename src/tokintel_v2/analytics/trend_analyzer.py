#!/usr/bin/env python3
# [REPORT] Trend Analyzer - TokIntel v2
# Analizza i trend personali dell'utente basati su parole chiave ed emozioni

import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
import logging
from pathlib import Path

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from db.database import get_db_manager
from core.logger import setup_logger

logger = setup_logger(__name__)

class TrendAnalyzer:
    """Analizzatore di trend personali per utenti"""
    
    def __init__(self):
        """Inizializza l'analizzatore"""
        self.db_manager = get_db_manager()
    
    def aggregate_keywords(self, user_id: int, days: int = 30) -> Dict[str, int]:
        """
        Aggrega le parole chiave più utilizzate nei video dell'utente
        
        Args:
            user_id: ID dell'utente
            days: Numero di giorni da considerare (default: 30)
            
        Returns:
            Dizionario con keyword e frequenza
        """
        try:
            # Recupera video analizzati dell'utente
            videos_with_analysis = self.db_manager.get_videos_with_analysis(user_id)
            
            # Filtra per periodo
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            recent_videos = [
                v for v in videos_with_analysis 
                if v['analyzed_at'] and v['analyzed_at'] > cutoff_date
            ]
            
            # Aggrega keywords
            keyword_counter = Counter()
            for video in recent_videos:
                if video['analysis'] and video['analysis'].get('keywords'):
                    # Gestisce sia stringhe che liste
                    keywords = video['analysis']['keywords']
                    if isinstance(keywords, str):
                        try:
                            keywords = json.loads(keywords)
                        except:
                            keywords = [keywords]
                    
                    if isinstance(keywords, list):
                        for keyword in keywords:
                            if keyword and isinstance(keyword, str):
                                keyword_counter[keyword.lower().strip()] += 1
            
            return dict(keyword_counter.most_common(20))
            
        except Exception as e:
            logger.error(f"Errore nell'aggregazione keywords: {e}")
            return {}
    
    def aggregate_emotions(self, user_id: int, days: int = 30) -> Dict[str, int]:
        """
        Aggrega le emozioni più frequenti nei video dell'utente
        
        Args:
            user_id: ID dell'utente
            days: Numero di giorni da considerare (default: 30)
            
        Returns:
            Dizionario con emozioni e frequenza
        """
        try:
            # Recupera video analizzati dell'utente
            videos_with_analysis = self.db_manager.get_videos_with_analysis(user_id)
            
            # Filtra per periodo
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            recent_videos = [
                v for v in videos_with_analysis 
                if v['analyzed_at'] and v['analyzed_at'] > cutoff_date
            ]
            
            # Lista di emozioni da cercare nel testo
            emotion_keywords = {
                'felicità': ['felice', 'contento', 'allegro', 'gioioso', 'sorriso', 'risata'],
                'tristezza': ['triste', 'malinconico', 'depresso', 'sconfortato', 'pianto'],
                'rabbia': ['arrabbiato', 'furioso', 'irritato', 'nervoso', 'stressato'],
                'paura': ['spaventato', 'terrorizzato', 'ansioso', 'preoccupato', 'nervoso'],
                'sorpresa': ['sorpreso', 'stupito', 'meravigliato', 'incredulo', 'sbalordito'],
                'disgusto': ['disgustato', 'nauseato', 'infastidito', 'repulso'],
                'amore': ['amore', 'affetto', 'passione', 'romantico', 'dolce'],
                'motivazione': ['motivato', 'ispirato', 'determinato', 'focalizzato', 'obiettivo'],
                'umore': ['divertente', 'comico', 'umoristico', 'scherzoso', 'ironico'],
                'calma': ['tranquillo', 'rilassato', 'sereno', 'pacifico', 'zen']
            }
            
            emotion_counter = Counter()
            
            for video in recent_videos:
                if video['analysis'] and video['analysis'].get('summary'):
                    summary = video['analysis']['summary'].lower()
                    
                    for emotion, keywords in emotion_keywords.items():
                        for keyword in keywords:
                            if keyword in summary:
                                emotion_counter[emotion] += 1
                                break  # Una sola emozione per video
            
            return dict(emotion_counter.most_common(10))
            
        except Exception as e:
            logger.error(f"Errore nell'aggregazione emozioni: {e}")
            return {}
    
    def trend_over_time(self, user_id: int, days: int = 90) -> pd.DataFrame:
        """
        Analizza i trend nel tempo per keywords ed emozioni
        
        Args:
            user_id: ID dell'utente
            days: Numero di giorni da considerare (default: 90)
            
        Returns:
            DataFrame con trend temporali
        """
        try:
            # Recupera video analizzati dell'utente
            videos_with_analysis = self.db_manager.get_videos_with_analysis(user_id)
            
            # Filtra per periodo
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            recent_videos = [
                v for v in videos_with_analysis 
                if v['analyzed_at'] and v['analyzed_at'] > cutoff_date
            ]
            
            # Prepara dati per DataFrame
            trend_data = []
            
            for video in recent_videos:
                if video['analysis']:
                    date = video['analyzed_at'].date()
                    
                    # Keywords
                    keywords = video['analysis'].get('keywords', [])
                    if isinstance(keywords, str):
                        try:
                            keywords = json.loads(keywords)
                        except:
                            keywords = [keywords]
                    
                    if isinstance(keywords, list):
                        for keyword in keywords:
                            if keyword and isinstance(keyword, str):
                                trend_data.append({
                                    'date': date,
                                    'type': 'keyword',
                                    'value': keyword.lower().strip(),
                                    'video_id': video['id']
                                })
                    
                    # Score come metrica di performance
                    score = video['analysis'].get('overall_score', 0)
                    trend_data.append({
                        'date': date,
                        'type': 'score',
                        'value': score,
                        'video_id': video['id']
                    })
            
            df = pd.DataFrame(trend_data)
            
            if df.empty:
                return pd.DataFrame(columns=['date', 'type', 'value', 'video_id'])
            
            return df
            
        except Exception as e:
            logger.error(f"Errore nell'analisi trend temporali: {e}")
            return pd.DataFrame()
    
    def get_user_insights(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Genera insights completi per l'utente
        
        Args:
            user_id: ID dell'utente
            days: Numero di giorni da considerare (default: 30)
            
        Returns:
            Dizionario con tutti gli insights
        """
        try:
            insights = {
                'keywords': self.aggregate_keywords(user_id, days),
                'emotions': self.aggregate_emotions(user_id, days),
                'trends': self.trend_over_time(user_id, days).to_dict('records'),
                'summary': {}
            }
            
            # Genera summary
            total_videos = len(self.db_manager.get_videos_by_status(user_id, 'analyzed'))
            top_keyword = max(insights['keywords'].items(), key=lambda x: x[1]) if insights['keywords'] else None
            top_emotion = max(insights['emotions'].items(), key=lambda x: x[1]) if insights['emotions'] else None
            
            insights['summary'] = {
                'total_analyzed_videos': total_videos,
                'top_keyword': top_keyword[0] if top_keyword else 'N/A',
                'top_keyword_count': top_keyword[1] if top_keyword else 0,
                'top_emotion': top_emotion[0] if top_emotion else 'N/A',
                'top_emotion_count': top_emotion[1] if top_emotion else 0,
                'analysis_period_days': days
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Errore nella generazione insights: {e}")
            return {
                'keywords': {},
                'emotions': {},
                'trends': [],
                'summary': {
                    'total_analyzed_videos': 0,
                    'top_keyword': 'N/A',
                    'top_keyword_count': 0,
                    'top_emotion': 'N/A',
                    'top_emotion_count': 0,
                    'analysis_period_days': days
                }
            }
    
    def get_content_themes(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """
        Identifica i temi principali del contenuto dell'utente
        
        Args:
            user_id: ID dell'utente
            days: Numero di giorni da considerare (default: 30)
            
        Returns:
            Lista di temi con metadati
        """
        try:
            keywords = self.aggregate_keywords(user_id, days)
            emotions = self.aggregate_emotions(user_id, days)
            
            # Categorizza keywords in temi
            themes = {
                'motivazione': ['motivazione', 'successo', 'obiettivo', 'determinazione', 'focus'],
                'intrattenimento': ['divertimento', 'comico', 'umorismo', 'risata', 'gioco'],
                'educazione': ['imparare', 'insegnamento', 'conoscenza', 'skill', 'tutorial'],
                'lifestyle': ['vita', 'quotidiano', 'routine', 'abitudini', 'benessere'],
                'tecnologia': ['tech', 'tecnologia', 'innovazione', 'digitale', 'app'],
                'business': ['business', 'lavoro', 'carriera', 'professione', 'impresa']
            }
            
            theme_scores = defaultdict(int)
            
            for keyword, count in keywords.items():
                for theme, theme_keywords in themes.items():
                    if any(theme_kw in keyword for theme_kw in theme_keywords):
                        theme_scores[theme] += count
            
            # Converti in lista ordinata
            theme_list = [
                {
                    'theme': theme,
                    'score': score,
                    'keywords': [kw for kw, count in keywords.items() 
                               if any(theme_kw in kw for theme_kw in themes.get(theme, []))]
                }
                for theme, score in sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
            ]
            
            return theme_list
            
        except Exception as e:
            logger.error(f"Errore nell'identificazione temi: {e}")
            return []

# Funzioni di utilità
def get_trend_analyzer() -> TrendAnalyzer:
    """Recupera un'istanza dell'analizzatore di trend"""
    return TrendAnalyzer()

def analyze_user_trends(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Funzione di utilità per analizzare i trend di un utente"""
    analyzer = get_trend_analyzer()
    return analyzer.get_user_insights(user_id, days) 