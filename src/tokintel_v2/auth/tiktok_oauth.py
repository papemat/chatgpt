#!/usr/bin/env python3
"""
TokIntel v2 - TikTok OAuth Authentication Module
Gestione login con TikTok via OAuth2 con fallback per cambiamenti API
"""

import os
import json
import logging
import requests
import webbrowser
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse
import time
import hashlib
import base64
import secrets

logger = logging.getLogger(__name__)

class TikTokOAuth:
    """Gestione autenticazione TikTok con OAuth2 e fallback"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Inizializza il client OAuth TikTok"""
        self.config = self._load_config(config_path)
        self.client_key = self.config.get('tiktok', {}).get('client_key')
        self.client_secret = self.config.get('tiktok', {}).get('client_secret')
        self.redirect_uri = self.config.get('tiktok', {}).get('redirect_uri', 'http://localhost:8501/auth/callback')
        self.scope = self.config.get('tiktok', {}).get('scope', 'user.info.basic,video.list')
        
        # Endpoints TikTok (con fallback)
        self.auth_url = "https://www.tiktok.com/v2/auth/authorize/"
        self.token_url = "https://open.tiktokapis.com/v2/oauth/token/"
        self.user_info_url = "https://open.tiktokapis.com/v2/user/info/"
        
        # Fallback endpoints (se l'API cambia)
        self.fallback_auth_url = "https://www.tiktok.com/oauth/authorize/"
        self.fallback_token_url = "https://open-api.tiktok.com/oauth/access_token/"
        self.fallback_user_info_url = "https://open-api.tiktok.com/user/info/"
        
        # Stato sessione
        self.access_token = None
        self.refresh_token = None
        self.user_info = None
        self.session_data = {}
        
        # File per persistenza
        self.session_file = Path("config/tiktok_session.json")
        self.session_file.parent.mkdir(exist_ok=True)
        
        logger.info("TikTok OAuth client initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carica configurazione da file"""
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load config from {config_path}: {e}")
            return {}
    
    def _save_session(self):
        """Salva dati sessione su file"""
        try:
            session_data = {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'user_info': self.user_info,
                'timestamp': time.time()
            }
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
            logger.info("Session data saved")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def _load_session(self) -> bool:
        """Carica dati sessione da file"""
        try:
            if not self.session_file.exists():
                return False
            
            with open(self.session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Verifica se la sessione è ancora valida (24 ore)
            if time.time() - session_data.get('timestamp', 0) > 86400:
                logger.info("Session expired, removing old session file")
                self.session_file.unlink()
                return False
            
            self.access_token = session_data.get('access_token')
            self.refresh_token = session_data.get('refresh_token')
            self.user_info = session_data.get('user_info')
            
            logger.info("Session data loaded")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return False
    
    def _generate_state(self) -> str:
        """Genera stato per sicurezza OAuth"""
        return secrets.token_urlsafe(32)
    
    def _generate_pkce(self) -> Tuple[str, str]:
        """Genera PKCE per sicurezza OAuth"""
        code_verifier = secrets.token_urlsafe(32)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip('=')
        return code_verifier, code_challenge
    
    def get_auth_url(self, use_fallback: bool = False) -> Tuple[str, str, str]:
        """
        Genera URL di autorizzazione TikTok
        
        Returns:
            Tuple[str, str, str]: (auth_url, state, code_verifier)
        """
        if not self.client_key:
            raise ValueError("TikTok client_key not configured")
        
        state = self._generate_state()
        code_verifier, code_challenge = self._generate_pkce()
        
        # Salva per verifica callback
        self.session_data = {
            'state': state,
            'code_verifier': code_verifier,
            'code_challenge': code_challenge
        }
        
        # Scegli endpoint (normale o fallback)
        base_auth_url = self.fallback_auth_url if use_fallback else self.auth_url
        
        params = {
            'client_key': self.client_key,
            'scope': self.scope,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"{base_auth_url}?{urlencode(params)}"
        logger.info(f"Generated auth URL (fallback: {use_fallback})")
        
        return auth_url, state, code_verifier
    
    def exchange_code_for_token(self, code: str, state: str, code_verifier: str, 
                               use_fallback: bool = False) -> bool:
        """
        Scambia codice autorizzazione per access token
        
        Args:
            code: Codice di autorizzazione
            state: Stato per verifica sicurezza
            code_verifier: Verificatore PKCE
            use_fallback: Usa endpoint fallback
            
        Returns:
            bool: True se successo
        """
        try:
            # Verifica stato
            if state != self.session_data.get('state'):
                raise ValueError("Invalid state parameter")
            
            # Verifica code_verifier
            if code_verifier != self.session_data.get('code_verifier'):
                raise ValueError("Invalid code verifier")
            
            # Scegli endpoint token
            token_endpoint = self.fallback_token_url if use_fallback else self.token_url
            
            data = {
                'client_key': self.client_key,
                'client_secret': self.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cache-Control': 'no-cache'
            }
            
            response = requests.post(token_endpoint, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'error' in token_data:
                raise ValueError(f"Token exchange failed: {token_data['error']}")
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            if not self.access_token:
                raise ValueError("No access token received")
            
            logger.info("Successfully obtained access token")
            self._save_session()
            return True
            
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            return False
    
    def refresh_access_token(self, use_fallback: bool = False) -> bool:
        """
        Aggiorna access token usando refresh token
        
        Args:
            use_fallback: Usa endpoint fallback
            
        Returns:
            bool: True se successo
        """
        if not self.refresh_token:
            logger.error("No refresh token available")
            return False
        
        try:
            token_endpoint = self.fallback_token_url if use_fallback else self.token_url
            
            data = {
                'client_key': self.client_key,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(token_endpoint, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'error' in token_data:
                raise ValueError(f"Token refresh failed: {token_data['error']}")
            
            self.access_token = token_data.get('access_token')
            if token_data.get('refresh_token'):
                self.refresh_token = token_data['refresh_token']
            
            logger.info("Successfully refreshed access token")
            self._save_session()
            return True
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return False
    
    def get_tiktok_user(self, use_fallback: bool = False) -> Optional[Dict[str, Any]]:
        """
        Recupera informazioni utente TikTok
        
        Args:
            use_fallback: Usa endpoint fallback
            
        Returns:
            Dict con info utente o None se errore
        """
        if not self.access_token:
            # Prova a caricare sessione salvata
            if not self._load_session():
                logger.error("No access token available")
                return None
        
        try:
            user_endpoint = self.fallback_user_info_url if use_fallback else self.user_info_url
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(user_endpoint, headers=headers)
            response.raise_for_status()
            
            user_data = response.json()
            
            if 'error' in user_data:
                raise ValueError(f"User info failed: {user_data['error']}")
            
            # Normalizza dati utente
            user_info = {
                'user_id': user_data.get('data', {}).get('user', {}).get('open_id'),
                'nickname': user_data.get('data', {}).get('user', {}).get('display_name'),
                'username': user_data.get('data', {}).get('user', {}).get('username'),
                'avatar_url': user_data.get('data', {}).get('user', {}).get('avatar_url'),
                'follower_count': user_data.get('data', {}).get('stats', {}).get('follower_count'),
                'following_count': user_data.get('data', {}).get('stats', {}).get('following_count'),
                'video_count': user_data.get('data', {}).get('stats', {}).get('video_count'),
                'likes_count': user_data.get('data', {}).get('stats', {}).get('likes_count')
            }
            
            self.user_info = user_info
            self._save_session()
            
            logger.info(f"Retrieved user info for: {user_info.get('nickname')}")
            return user_info
            
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Verifica se l'utente è autenticato"""
        if not self.access_token:
            return self._load_session()
        return True
    
    def logout(self):
        """Logout e pulizia sessione"""
        self.access_token = None
        self.refresh_token = None
        self.user_info = None
        self.session_data = {}
        
        if self.session_file.exists():
            self.session_file.unlink()
        
        logger.info("User logged out")
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Restituisce stato autenticazione"""
        return {
            'authenticated': self.is_authenticated(),
            'has_access_token': bool(self.access_token),
            'has_refresh_token': bool(self.refresh_token),
            'user_info': self.user_info,
            'session_file_exists': self.session_file.exists()
        } 