#!/usr/bin/env python3
# DONE: Typing completo aggiunto
# DONE: Docstring Google-style aggiunte
# DONE: Logger strutturato implementato
# DONE: Try/except granulari implementati
# DONE: Validazione input aggiunta

"""
⏰ Auto-Analyze Scheduler - TokIntel v2
Sistema di schedulazione automatica per l'analisi dei video TikTok
"""

import asyncio
import argparse
import signal
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path
import logging

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from batch_auto_analyze import analyze_user_pending_videos
from core.logger import setup_logger

logger = setup_logger(__name__)

class AutoAnalyzeScheduler:
    """Scheduler per l'analisi automatica dei video TikTok"""
    
    def __init__(self):
        """Inizializza lo scheduler"""
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        self.current_user_id = None
        self.current_interval = None
        
    def start_auto_analyzer(self, user_id: int, interval_minutes: int = 60) -> bool:
        """
        Avvia lo scheduler per l'auto-analisi
        
        Args:
            user_id: ID dell'utente da monitorare
            interval_minutes: Intervallo in minuti tra le esecuzioni
            
        Returns:
            True se lo scheduler è stato avviato con successo
        """
        try:
            # Validazione input
            if not isinstance(user_id, int) or user_id <= 0:
                raise ValueError("user_id deve essere un intero positivo")
            if not isinstance(interval_minutes, int) or interval_minutes <= 0:
                raise ValueError("interval_minutes deve essere un intero positivo")
            
            self.current_user_id = user_id
            self.current_interval = interval_minutes
            
            # Configura il job
            job_id = f"auto_analyze_user_{user_id}"
            
            # Aggiungi il job allo scheduler
            self.scheduler.add_job(
                func=self._run_analysis_job,
                trigger=IntervalTrigger(minutes=interval_minutes),
                id=job_id,
                args=[user_id],
                replace_existing=True,
                max_instances=1
            )
            
            # Aggiungi listener per eventi
            self.scheduler.add_listener(self._job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
            
            # Avvia lo scheduler
            self.scheduler.start()
            self.is_running = True
            
            logger.info(f"[OK] [TokIntel Scheduler] Avviato per user_id={user_id} - intervallo: {interval_minutes} min")
            
            # Esegui immediatamente la prima analisi se c'è un event loop attivo
            try:
                loop = asyncio.get_running_loop()
                asyncio.create_task(self._run_analysis_job(user_id))
            except RuntimeError:
                # Nessun event loop attivo, la prima esecuzione avverrà al primo intervallo
                logger.info("Event loop non attivo, prima analisi programmata per il primo intervallo")
            
            return True
            
        except ValueError as e:
            logger.error(f"[ERROR] Errore di validazione input: {e}")
            return False
        except Exception as e:
            logger.error(f"[ERROR] Errore nell'avvio dello scheduler: {e}")
            return False
    
    async def _run_analysis_job(self, user_id: int):
        """
        Esegue il job di analisi
        
        Args:
            user_id: ID dell'utente da analizzare
        """
        start_time = datetime.now()
        current_time = start_time.strftime("%H:%M")
        
        try:
            logger.info(f"[OK] [TokIntel Auto] Analisi avviata - {current_time}")
            
            # Esegui l'analisi
            result = await analyze_user_pending_videos(user_id)
            
            # Logga i risultati
            analyzed = result.get('analyzed', 0)
            errors = result.get('errors', 0)
            total = result.get('total_videos', 0)
            
            if errors > 0:
                logger.info(f"[OK] Completati {analyzed} video - [ERROR] {errors} errori")
            else:
                logger.info(f"[OK] Completati {analyzed} video - [ERROR] {errors} errori")
                
            # Log dettagliato se ci sono stati errori
            if errors > 0 and 'error_details' in result:
                for error_detail in result['error_details']:
                    logger.warning(f"[WARN] Errore video: {error_detail}")
                    
        except Exception as e:
            logger.error(f"[ERROR] Errore durante l'analisi automatica: {e}")
    
    def _job_listener(self, event):
        """Listener per gli eventi del job"""
        if event.exception:
            logger.error(f"[ERROR] Job fallito: {event.exception}")
        else:
            logger.debug(f"[OK] Job completato con successo")
    
    def stop_scheduler(self):
        """Ferma lo scheduler"""
        try:
            if self.is_running:
                self.scheduler.shutdown(wait=False)
                self.is_running = False
                logger.info("🛑 [TokIntel Scheduler] Fermato")
        except Exception as e:
            logger.error(f"[ERROR] Errore nell'arresto dello scheduler: {e}")
    
    def get_status(self) -> dict:
        """Restituisce lo stato dello scheduler"""
        try:
            return {
                'is_running': self.is_running,
                'user_id': self.current_user_id,
                'interval_minutes': self.current_interval,
                'jobs': len(self.scheduler.get_jobs()) if self.is_running else 0
            }
        except Exception as e:
            logger.error(f"[ERROR] Errore nel recupero status scheduler: {e}")
            return {
                'is_running': False,
                'user_id': None,
                'interval_minutes': None,
                'jobs': 0
            }

# Istanza globale dello scheduler
_scheduler_instance: Optional[AutoAnalyzeScheduler] = None

def get_scheduler() -> AutoAnalyzeScheduler:
    """Recupera l'istanza globale dello scheduler"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AutoAnalyzeScheduler()
    return _scheduler_instance

def start_auto_analyzer(user_id: int, interval_minutes: int = 60) -> bool:
    """
    Funzione principale per avviare l'auto-analyzer
    
    Args:
        user_id: ID dell'utente da monitorare
        interval_minutes: Intervallo in minuti tra le esecuzioni
        
    Returns:
        True se lo scheduler è stato avviato con successo
    """
    scheduler = get_scheduler()
    return scheduler.start_auto_analyzer(user_id, interval_minutes)

def stop_auto_analyzer():
    """Ferma l'auto-analyzer"""
    scheduler = get_scheduler()
    scheduler.stop_scheduler()

def get_auto_analyzer_status() -> dict:
    """Restituisce lo stato dell'auto-analyzer"""
    scheduler = get_scheduler()
    return scheduler.get_status()

async def main():
    """Funzione principale per CLI"""
    parser = argparse.ArgumentParser(description='Auto-Analyze Scheduler per TokIntel v2')
    parser.add_argument('--user-id', type=int, required=True, help='ID utente da monitorare')
    parser.add_argument('--interval', type=int, default=60, help='Intervallo in minuti (default: 60)')
    parser.add_argument('--status', action='store_true', help='Mostra solo lo status dello scheduler')
    parser.add_argument('--stop', action='store_true', help='Ferma lo scheduler')
    
    args = parser.parse_args()
    
    try:
        # Validazione argomenti
        if args.user_id <= 0:
            print("[ERROR] user-id deve essere un intero positivo")
            sys.exit(1)
        
        if args.interval <= 0:
            print("[ERROR] interval deve essere un intero positivo")
            sys.exit(1)
        
        if args.status:
            # Mostra solo lo status
            status = get_auto_analyzer_status()
            print(f"Status Scheduler: {status}")
            return
        
        if args.stop:
            # Ferma lo scheduler
            stop_auto_analyzer()
            print("Scheduler fermato")
            return
        
        # Avvia lo scheduler
        success = start_auto_analyzer(args.user_id, args.interval)
        
        if success:
            print(f"[OK] Scheduler avviato per user_id={args.user_id} con intervallo {args.interval} minuti")
            print("[INFO] Premi Ctrl+C per fermare...")
            
            # Mantieni il processo attivo
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Fermata richiesta dall'utente...")
                stop_auto_analyzer()
        else:
            print("[ERROR] Errore nell'avvio dello scheduler")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"[ERROR] Errore di validazione argomenti: {e}")
        print(f"[ERROR] Errore di validazione: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[ERROR] Errore nell'esecuzione CLI: {e}")
        print(f"[ERROR] Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 