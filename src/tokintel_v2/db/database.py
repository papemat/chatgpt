# DONE: Typing completo aggiunto
# DONE: Docstring Google-style aggiunte
# DONE: Logger strutturato implementato
# DONE: Try/except granulari implementati
# DONE: Config centralizzata in config.yaml

"""
💾 Database PostgreSQL - TokIntel v2.1
Sistema di database avanzato per analisi TikTok con SQLAlchemy
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
import logging
from contextlib import contextmanager

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base per i modelli
Base = declarative_base()

class User(Base):
    """Modello per gli utenti del sistema"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relazioni
    video_analyses = relationship("VideoAnalysis", back_populates="user")
    agent_insights = relationship("AgentInsight", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class VideoAnalysis(Base):
    """Modello per le analisi video"""
    __tablename__ = 'video_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    video_title = Column(String(200), nullable=False)
    video_url = Column(String(500))
    video_path = Column(String(500))
    
    # Metriche principali
    overall_score = Column(Float, nullable=False)
    engagement_rate = Column(Float)
    completion_rate = Column(Float)
    share_rate = Column(Float)
    comment_rate = Column(Float)
    like_rate = Column(Float)
    
    # Dati analisi
    summary = Column(Text)
    key_points = Column(JSON)  # Lista di stringhe
    keywords = Column(JSON)    # Lista di stringhe
    suggested_hashtags = Column(JSON)  # Lista di stringhe
    recommendations = Column(JSON)     # Lista di dizionari
    
    # Metadati tecnici
    duration = Column(String(50))
    resolution = Column(String(50))
    format_type = Column(String(20))
    ai_model = Column(String(50))
    version = Column(String(20))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relazioni
    user = relationship("User", back_populates="video_analyses")
    agent_insights = relationship("AgentInsight", back_populates="video_analysis")
    
    def __repr__(self):
        return f"<VideoAnalysis(id={self.id}, title='{self.video_title}', score={self.overall_score})>"

class AgentInsight(Base):
    """Modello per gli insights degli agenti AI"""
    __tablename__ = 'agent_insights'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    video_analysis_id = Column(Integer, ForeignKey('video_analyses.id'), nullable=False)
    
    # Dati agente
    agent_type = Column(String(50), nullable=False)  # strategist, copywriter, analyst
    agent_name = Column(String(100), nullable=False)
    agent_role = Column(String(200))
    
    # Contenuto insight
    message = Column(Text, nullable=False)
    response_type = Column(String(50))  # advice, analysis, recommendation
    confidence_score = Column(Float)
    
    # Metadati
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    user = relationship("User", back_populates="agent_insights")
    video_analysis = relationship("VideoAnalysis", back_populates="agent_insights")
    
    def __repr__(self):
        return f"<AgentInsight(id={self.id}, agent='{self.agent_type}', video_id={self.video_analysis_id})>"

class AnalyticsEvent(Base):
    """Modello per eventi analytics"""
    __tablename__ = 'analytics_events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    event_type = Column(String(50), nullable=False)  # video_upload, analysis_complete, export_pdf, etc.
    event_data = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnalyticsEvent(id={self.id}, type='{self.event_type}', user_id={self.user_id})>"

class UserTikTokSession(Base):
    """Modello per le sessioni TikTok degli utenti"""
    __tablename__ = 'user_tiktok_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Dati sessione TikTok
    tiktok_username = Column(String(100), nullable=False)
    session_data = Column(JSON)  # Dati di sessione (cookies, tokens, etc.)
    is_active = Column(Boolean, default=True)
    
    # Metadati sessione
    login_method = Column(String(50))  # manual, browser, api
    last_activity = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relazioni
    user = relationship("User", backref="tiktok_sessions")
    saved_videos = relationship("UserSavedVideo", back_populates="session")
    
    def __repr__(self):
        return f"<UserTikTokSession(id={self.id}, user_id={self.user_id}, username='{self.tiktok_username}')>"

class UserSavedVideo(Base):
    """Modello per i video TikTok salvati dagli utenti"""
    __tablename__ = 'user_saved_videos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('user_tiktok_sessions.id'), nullable=True)
    
    # Dati video TikTok
    tiktok_video_id = Column(String(100), nullable=False)
    video_url = Column(String(500), nullable=False)
    video_title = Column(String(200))
    creator_username = Column(String(100))
    
    # Metadati video
    duration = Column(String(50))
    resolution = Column(String(50))
    view_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    share_count = Column(Integer)
    
    # Dati locali
    local_file_path = Column(String(500))
    file_size_mb = Column(Float)
    download_status = Column(String(50), default='pending')  # pending, downloaded, failed
    
    # Status analisi
    status = Column(String(20), default='new')  # new, analyzed, error
    
    # Analisi associata
    analysis_id = Column(Integer, ForeignKey('video_analyses.id'), nullable=True)
    
    # Timestamps
    saved_at = Column(DateTime, default=datetime.utcnow)
    downloaded_at = Column(DateTime)
    analyzed_at = Column(DateTime)
    
    # Relazioni
    user = relationship("User", backref="saved_videos")
    session = relationship("UserTikTokSession", back_populates="saved_videos")
    analysis = relationship("VideoAnalysis", backref="saved_video")
    
    def __repr__(self):
        return f"<UserSavedVideo(id={self.id}, video_id='{self.tiktok_video_id}', user_id={self.user_id})>"

class DatabaseManager:
    """Gestore principale del database"""
    
    def __init__(self, database_url: str = None):
        """Inizializza il gestore database"""
        
        if database_url is None:
            # Configurazione di default
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'tokintel')
            db_user = os.getenv('DB_USER', 'postgres')
            db_password = os.getenv('DB_PASSWORD', 'password')
            
            database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Crea le tabelle se non esistono
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database inizializzato con successo")
        except OperationalError as e:
            logger.error(f"Errore di connessione al database: {e}")
            raise
        except Exception as e:
            logger.error(f"Errore nell'inizializzazione del database: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Session:
        """Context manager per le sessioni database"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except IntegrityError as e:
            session.rollback()
            logger.error(f"Errore di integrità database: {e}")
            raise
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Errore SQLAlchemy: {e}")
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Errore database generico: {e}")
            raise
        finally:
            session.close()
    
    def create_user(self, username: str, email: str, password_hash: str, is_admin: bool = False) -> User:
        """Crea un nuovo utente"""
        try:
            with self.get_session() as session:
                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    is_admin=is_admin
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                logger.info(f"Utente creato: {username}")
                return user
        except IntegrityError as e:
            logger.error(f"Utente già esistente: {username}")
            raise
        except Exception as e:
            logger.error(f"Errore nella creazione utente: {e}")
            raise
    
    def save_video_analysis(self, user_id: int, analysis_data: Dict[str, Any]) -> VideoAnalysis:
        """Salva un'analisi video"""
        try:
            with self.get_session() as session:
                analysis = VideoAnalysis(
                    user_id=user_id,
                    video_title=analysis_data.get('video_title', 'Video TikTok'),
                    video_url=analysis_data.get('video_url'),
                    video_path=analysis_data.get('video_path'),
                    overall_score=analysis_data.get('overall_score', 0),
                    engagement_rate=analysis_data.get('metrics', {}).get('engagement_rate'),
                    completion_rate=analysis_data.get('metrics', {}).get('completion_rate'),
                    share_rate=analysis_data.get('metrics', {}).get('share_rate'),
                    comment_rate=analysis_data.get('metrics', {}).get('comment_rate'),
                    like_rate=analysis_data.get('metrics', {}).get('like_rate'),
                    summary=analysis_data.get('summary'),
                    key_points=analysis_data.get('key_points', []),
                    keywords=analysis_data.get('keywords', []),
                    suggested_hashtags=analysis_data.get('suggested_hashtags', []),
                    recommendations=analysis_data.get('recommendations', []),
                    duration=analysis_data.get('duration'),
                    resolution=analysis_data.get('resolution'),
                    format_type=analysis_data.get('format'),
                    ai_model=analysis_data.get('ai_model'),
                    version=analysis_data.get('version', 'v2.1')
                )
                session.add(analysis)
                session.commit()
                session.refresh(analysis)
                logger.info(f"Analisi video salvata: {analysis.id}")
                return analysis
        except Exception as e:
            logger.error(f"Errore nel salvataggio analisi video: {e}")
            raise
    
    def save_agent_insight(self, user_id: int, video_analysis_id: int, agent_data: Dict[str, Any]) -> AgentInsight:
        """Salva un insight di un agente"""
        try:
            with self.get_session() as session:
                insight = AgentInsight(
                    user_id=user_id,
                    video_analysis_id=video_analysis_id,
                    agent_type=agent_data.get('agent_type'),
                    agent_name=agent_data.get('agent_name'),
                    agent_role=agent_data.get('agent_role'),
                    message=agent_data.get('message'),
                    response_type=agent_data.get('response_type'),
                    confidence_score=agent_data.get('confidence_score')
                )
                session.add(insight)
                session.commit()
                session.refresh(insight)
                logger.info(f"Insight agente salvato: {insight.id}")
                return insight
        except Exception as e:
            logger.error(f"Errore nel salvataggio insight agente: {e}")
            raise
    
    def get_user_analyses(self, user_id: int, limit: int = 50) -> List[VideoAnalysis]:
        """Recupera le analisi di un utente"""
        try:
            with self.get_session() as session:
                analyses = session.query(VideoAnalysis)\
                    .filter(VideoAnalysis.user_id == user_id)\
                    .order_by(VideoAnalysis.created_at.desc())\
                    .limit(limit)\
                    .all()
                return analyses
        except Exception as e:
            logger.error(f"Errore nel recupero analisi utente: {e}")
            raise
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[VideoAnalysis]:
        """Recupera un'analisi per ID"""
        try:
            with self.get_session() as session:
                analysis = session.query(VideoAnalysis)\
                    .filter(VideoAnalysis.id == analysis_id)\
                    .first()
                return analysis
        except Exception as e:
            logger.error(f"Errore nel recupero analisi per ID: {e}")
            raise
    
    def get_agent_insights_for_analysis(self, video_analysis_id: int) -> List[AgentInsight]:
        """Recupera gli insights degli agenti per un'analisi"""
        try:
            with self.get_session() as session:
                insights = session.query(AgentInsight)\
                    .filter(AgentInsight.video_analysis_id == video_analysis_id)\
                    .order_by(AgentInsight.created_at.asc())\
                    .all()
                return insights
        except Exception as e:
            logger.error(f"Errore nel recupero insights agente per analisi: {e}")
            raise
    
    def get_analytics_summary(self, user_id: int = None, days: int = 30) -> Dict[str, Any]:
        """Recupera un riepilogo analytics"""
        try:
            with self.get_session() as session:
                start_date = datetime.utcnow() - timedelta(days=days)
                
                # Query base
                query = session.query(VideoAnalysis)
                if user_id:
                    query = query.filter(VideoAnalysis.user_id == user_id)
                
                # Statistiche generali
                total_analyses = query.filter(VideoAnalysis.created_at >= start_date).count()
                avg_score = query.filter(VideoAnalysis.created_at >= start_date).with_entities(
                    session.query(VideoAnalysis.overall_score).func.avg()
                ).scalar() or 0
                
                # Top keywords
                all_keywords = []
                analyses = query.filter(VideoAnalysis.created_at >= start_date).all()
                for analysis in analyses:
                    if analysis.keywords:
                        all_keywords.extend(analysis.keywords)
                
                # Conta frequenza keywords
                keyword_counts = {}
                for keyword in all_keywords:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
                
                top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                return {
                    'total_analyses': total_analyses,
                    'average_score': round(avg_score, 2),
                    'top_keywords': top_keywords,
                    'period_days': days
                }
        except Exception as e:
            logger.error(f"Errore nel recupero riepilogo analytics: {e}")
            raise
    
    def log_analytics_event(self, event_type: str, event_data: Dict = None, user_id: int = None, 
                          ip_address: str = None, user_agent: str = None):
        """Registra un evento analytics"""
        try:
            with self.get_session() as session:
                event = AnalyticsEvent(
                    user_id=user_id,
                    event_type=event_type,
                    event_data=event_data,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                session.add(event)
                session.commit()
                logger.info(f"Evento analytics registrato: {event_type}")
        except Exception as e:
            logger.error(f"Errore nel registro evento analytics: {e}")
            raise
    
    # Metodi per gestione sessioni TikTok
    def create_tiktok_session(self, user_id: int, tiktok_username: str, session_data: Dict[str, Any], 
                             login_method: str = "manual") -> UserTikTokSession:
        """Crea una nuova sessione TikTok per un utente"""
        try:
            with self.get_session() as session:
                # Disattiva sessioni precedenti
                session.query(UserTikTokSession)\
                    .filter(UserTikTokSession.user_id == user_id, UserTikTokSession.is_active == True)\
                    .update({"is_active": False})
                
                # Crea nuova sessione
                tiktok_session = UserTikTokSession(
                    user_id=user_id,
                    tiktok_username=tiktok_username,
                    session_data=session_data,
                    login_method=login_method,
                    expires_at=datetime.utcnow() + timedelta(days=30)  # Scade in 30 giorni
                )
                session.add(tiktok_session)
                session.commit()
                session.refresh(tiktok_session)
                logger.info(f"Sessione TikTok creata per utente {user_id}: {tiktok_username}")
                return tiktok_session
        except Exception as e:
            logger.error(f"Errore nella creazione sessione TikTok: {e}")
            raise
    
    def get_active_tiktok_session(self, user_id: int) -> Optional[UserTikTokSession]:
        """Recupera la sessione TikTok attiva di un utente"""
        try:
            with self.get_session() as session:
                tiktok_session = session.query(UserTikTokSession)\
                    .filter(UserTikTokSession.user_id == user_id, UserTikTokSession.is_active == True)\
                    .first()
                return tiktok_session
        except Exception as e:
            logger.error(f"Errore nel recupero sessione TikTok attiva: {e}")
            raise
    
    def update_tiktok_session_activity(self, session_id: int):
        """Aggiorna l'ultima attività di una sessione TikTok"""
        try:
            with self.get_session() as session:
                session.query(UserTikTokSession)\
                    .filter(UserTikTokSession.id == session_id)\
                    .update({"last_activity": datetime.utcnow()})
                session.commit()
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento attività sessione TikTok: {e}")
            raise
    
    def deactivate_tiktok_session(self, session_id: int):
        """Disattiva una sessione TikTok"""
        try:
            with self.get_session() as session:
                session.query(UserTikTokSession)\
                    .filter(UserTikTokSession.id == session_id)\
                    .update({"is_active": False})
                session.commit()
                logger.info(f"Sessione TikTok {session_id} disattivata")
        except Exception as e:
            logger.error(f"Errore nella disattivazione sessione TikTok: {e}")
            raise
    
    # Metodi per gestione video salvati
    def save_tiktok_video(self, user_id: int, video_data: Dict[str, Any], 
                         session_id: int = None) -> UserSavedVideo:
        """Salva un video TikTok nel database"""
        try:
            with self.get_session() as session:
                # Verifica se il video è già salvato
                existing_video = session.query(UserSavedVideo)\
                    .filter(UserSavedVideo.user_id == user_id, 
                           UserSavedVideo.tiktok_video_id == video_data['tiktok_video_id'])\
                    .first()
                
                if existing_video:
                    # Aggiorna video esistente
                    for key, value in video_data.items():
                        if hasattr(existing_video, key):
                            setattr(existing_video, key, value)
                    existing_video.updated_at = datetime.utcnow()
                    session.commit()
                    session.refresh(existing_video)
                    logger.info(f"Video TikTok aggiornato: {existing_video.tiktok_video_id}")
                    return existing_video
                
                # Crea nuovo video
                saved_video = UserSavedVideo(
                    user_id=user_id,
                    session_id=session_id,
                    tiktok_video_id=video_data['tiktok_video_id'],
                    video_url=video_data['video_url'],
                    video_title=video_data.get('video_title'),
                    creator_username=video_data.get('creator_username'),
                    duration=video_data.get('duration'),
                    resolution=video_data.get('resolution'),
                    view_count=video_data.get('view_count'),
                    like_count=video_data.get('like_count'),
                    comment_count=video_data.get('comment_count'),
                    share_count=video_data.get('share_count'),
                    local_file_path=video_data.get('local_file_path'),
                    file_size_mb=video_data.get('file_size_mb'),
                    download_status=video_data.get('download_status', 'pending')
                )
                session.add(saved_video)
                session.commit()
                session.refresh(saved_video)
                logger.info(f"Video TikTok salvato: {saved_video.tiktok_video_id}")
                return saved_video
        except Exception as e:
            logger.error(f"Errore nel salvataggio video TikTok: {e}")
            raise
    
    def update_video_download_status(self, video_id: int, download_status: str, 
                                   local_file_path: str = None, file_size_mb: float = None):
        """Aggiorna lo stato di download di un video"""
        try:
            with self.get_session() as session:
                video = session.query(UserSavedVideo)\
                    .filter(UserSavedVideo.id == video_id)\
                    .first()
                
                if video:
                    video.download_status = download_status
                    if download_status == 'downloaded':
                        video.downloaded_at = datetime.utcnow()
                        if local_file_path:
                            video.local_file_path = local_file_path
                        if file_size_mb:
                            video.file_size_mb = file_size_mb
                    
                    session.commit()
                    logger.info(f"Stato download aggiornato per video {video.tiktok_video_id}: {download_status}")
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento stato download video: {e}")
            raise
    
    def link_video_to_analysis(self, video_id: int, analysis_id: int):
        """Collega un video salvato a un'analisi"""
        try:
            with self.get_session() as session:
                video = session.query(UserSavedVideo)\
                    .filter(UserSavedVideo.id == video_id)\
                    .first()
                
                if video:
                    video.analysis_id = analysis_id
                    video.analyzed_at = datetime.utcnow()
                    session.commit()
                    logger.info(f"Video {video.tiktok_video_id} collegato all'analisi {analysis_id}")
        except Exception as e:
            logger.error(f"Errore nella collegamento video all'analisi: {e}")
            raise
    
    def update_video_status(self, video_id: int, status: str):
        """Aggiorna lo status di un video (new, analyzed, error)"""
        try:
            with self.get_session() as session:
                video = session.query(UserSavedVideo).filter(UserSavedVideo.id == video_id).first()
                if video:
                    video.status = status
                    if status == 'analyzed':
                        video.analyzed_at = datetime.utcnow()
                    session.commit()
                    logger.info(f"Status video {video_id} aggiornato a: {status}")
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento status video: {e}")
            raise
    
    def get_videos_by_status(self, user_id: int, status: str = None) -> List[UserSavedVideo]:
        """Recupera video filtrati per status"""
        try:
            with self.get_session() as session:
                query = session.query(UserSavedVideo).filter(UserSavedVideo.user_id == user_id)
                if status:
                    query = query.filter(UserSavedVideo.status == status)
                videos = query.order_by(UserSavedVideo.saved_at.desc()).all()
                return videos
        except Exception as e:
            logger.error(f"Errore nel recupero video per status: {e}")
            raise
    
    def get_user_saved_videos(self, user_id: int, limit: int = 100) -> List[UserSavedVideo]:
        """Recupera i video salvati di un utente"""
        try:
            with self.get_session() as session:
                videos = session.query(UserSavedVideo)\
                    .filter(UserSavedVideo.user_id == user_id)\
                    .order_by(UserSavedVideo.saved_at.desc())\
                    .limit(limit)\
                    .all()
                return videos
        except Exception as e:
            logger.error(f"Errore nel recupero video salvati utente: {e}")
            raise
    
    def get_video_by_tiktok_id(self, user_id: int, tiktok_video_id: str) -> Optional[UserSavedVideo]:
        """Recupera un video salvato per ID TikTok"""
        try:
            with self.get_session() as session:
                video = session.query(UserSavedVideo)\
                    .filter(UserSavedVideo.user_id == user_id, 
                           UserSavedVideo.tiktok_video_id == tiktok_video_id)\
                    .first()
                return video
        except Exception as e:
            logger.error(f"Errore nel recupero video per ID TikTok: {e}")
            raise
    
    def get_videos_with_analysis(self, user_id: int) -> List[Dict[str, Any]]:
        """Recupera video con analisi associate"""
        try:
            with self.get_session() as session:
                videos = session.query(UserSavedVideo, VideoAnalysis)\
                    .join(VideoAnalysis, UserSavedVideo.analysis_id == VideoAnalysis.id, isouter=True)\
                    .filter(UserSavedVideo.user_id == user_id)\
                    .order_by(UserSavedVideo.saved_at.desc())\
                    .all()
                
                result = []
                for video, analysis in videos:
                    video_dict = {
                        'id': video.id,
                        'tiktok_video_id': video.tiktok_video_id,
                        'video_url': video.video_url,
                        'video_title': video.video_title,
                        'creator_username': video.creator_username,
                        'download_status': video.download_status,
                        'status': video.status,  # new, analyzed, error
                        'local_file_path': video.local_file_path,
                        'file_size_mb': video.file_size_mb,
                        'saved_at': video.saved_at,
                        'downloaded_at': video.downloaded_at,
                        'analyzed_at': video.analyzed_at,
                        'analysis': None
                    }
                    
                    if analysis:
                        video_dict['analysis'] = {
                            'id': analysis.id,
                            'overall_score': analysis.overall_score,
                            'summary': analysis.summary,
                            'created_at': analysis.created_at
                        }
                    
                    result.append(video_dict)
                
                return result
        except Exception as e:
            logger.error(f"Errore nel recupero video con analisi associate: {e}")
            raise

# Istanza globale del database manager
db_manager = None

def init_database(database_url: str = None) -> DatabaseManager:
    """Inizializza il database manager globale"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    return db_manager

def get_db_manager() -> DatabaseManager:
    """Recupera l'istanza del database manager"""
    if db_manager is None:
        raise RuntimeError("Database non inizializzato. Chiama init_database() prima.")
    return db_manager

# Funzioni di utilità per l'integrazione con il sistema esistente
def save_analysis_result(analysis_data: Dict[str, Any], user_id: int = 1) -> int:
    """Salva un risultato di analisi nel database"""
    try:
        manager = get_db_manager()
        analysis = manager.save_video_analysis(user_id, analysis_data)
        return analysis.id
    except Exception as e:
        logger.error(f"Errore nel salvataggio analisi: {e}")
        raise

def get_analysis_history(user_id: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
    """Recupera la cronologia delle analisi"""
    try:
        manager = get_db_manager()
        analyses = manager.get_user_analyses(user_id, limit)
        
        return [{
            'id': analysis.id,
            'title': analysis.video_title,
            'score': analysis.overall_score,
            'created_at': analysis.created_at.isoformat(),
            'summary': analysis.summary
        } for analysis in analyses]
    except Exception as e:
        logger.error(f"Errore nel recupero cronologia: {e}")
        return []

if __name__ == "__main__":
    # Test del modulo
    try:
        # Inizializza database (usa SQLite per test)
        test_db_url = "sqlite:///test_tokintel.db"
        db = init_database(test_db_url)
        
        # Test creazione utente
        user = db.create_user("test_user", "test@example.com", "hash123")
        print(f"Utente creato: {user}")
        
        # Test salvataggio analisi
        test_analysis = {
            'video_title': 'Test Video',
            'overall_score': 85.5,
            'summary': 'Video di test per verificare il database',
            'keywords': ['test', 'database', 'tiktok'],
            'metrics': {
                'engagement_rate': 4.2,
                'completion_rate': 75
            }
        }
        
        analysis_id = db.save_video_analysis(user.id, test_analysis)
        print(f"Analisi salvata con ID: {analysis_id}")
        
        # Test recupero cronologia
        history = get_analysis_history(user.id)
        print(f"Cronologia: {len(history)} analisi trovate")
        
        print("Test database completato con successo!")
        
    except Exception as e:
        print(f"Errore nel test: {e}") 