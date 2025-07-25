"""
[REPORT] PDF Exporter - TokIntel v2.1
Generatore di report PDF professionali per analisi TikTok
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from fpdf import FPDF
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokIntelPDF(FPDF):
    """Classe personalizzata per generare PDF TokIntel"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        
        # Colori TokIntel
        self.primary_color = (41, 128, 185)  # Blu
        self.secondary_color = (52, 152, 219)  # Azzurro
        self.accent_color = (231, 76, 60)  # Rosso
        
    def header(self):
        """Header personalizzato per ogni pagina"""
        self.set_font('Arial', 'B', 15)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, 'TokIntel v2.1 - Report Analisi TikTok', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Footer personalizzato"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', 0, 0, 'C')
        self.cell(0, 10, f'Generato il {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'R')

class PDFExporter:
    """Esportatore PDF per report TokIntel"""
    
    def __init__(self):
        self.pdf = TokIntelPDF()
        self.pdf.alias_nb_pages()
        
    def create_report(self, analysis_data: Dict[str, Any], output_path: str = None) -> str:
        """Crea un report PDF completo"""
        
        try:
            # Titolo principale
            self._add_title_page(analysis_data)
            
            # Sezione sintesi
            self._add_summary_section(analysis_data)
            
            # Sezione metriche
            self._add_metrics_section(analysis_data)
            
            # Sezione keywords
            self._add_keywords_section(analysis_data)
            
            # Sezione consigli
            self._add_recommendations_section(analysis_data)
            
            # Sezione tecnica
            self._add_technical_section(analysis_data)
            
            # Genera file
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"tokintel_report_{timestamp}.pdf"
            
            self.pdf.output(output_path)
            logger.info(f"Report PDF generato: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Errore nella generazione PDF: {e}")
            raise
    
    def _add_title_page(self, data: Dict[str, Any]):
        """Aggiunge la pagina del titolo"""
        self.pdf.add_page()
        
        # Logo/Titolo
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 20, 'TokIntel v2.1', 0, 1, 'C')
        
        self.pdf.set_font('Arial', 'B', 18)
        self.pdf.cell(0, 15, 'Report Analisi TikTok', 0, 1, 'C')
        
        # Informazioni video
        self.pdf.ln(20)
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.secondary_color)
        
        video_title = data.get('video_title', 'Video TikTok')
        self.pdf.cell(0, 10, f'Video: {video_title}', 0, 1, 'L')
        
        # Data analisi
        analysis_date = data.get('analysis_date', datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(0)
        self.pdf.cell(0, 10, f'Data Analisi: {analysis_date}', 0, 1, 'L')
        
        # Score generale
        score = data.get('overall_score', 0)
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.accent_color)
        self.pdf.cell(0, 15, f'Score Generale: {score}/100', 0, 1, 'C')
    
    def _add_summary_section(self, data: Dict[str, Any]):
        """Aggiunge la sezione sintesi"""
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 15, '[INFO] Sintesi Analisi', 0, 1, 'L')
        
        # Sintesi testuale
        summary = data.get('summary', 'Nessuna sintesi disponibile.')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(0)
        self.pdf.multi_cell(0, 8, summary)
        
        # Punti chiave
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.secondary_color)
        self.pdf.cell(0, 10, 'Punti Chiave:', 0, 1, 'L')
        
        key_points = data.get('key_points', [])
        self.pdf.set_font('Arial', '', 11)
        self.pdf.set_text_color(0)
        
        for point in key_points:
            self.pdf.cell(10, 8, '•', 0, 0)
            self.pdf.multi_cell(0, 8, point)
    
    def _add_metrics_section(self, data: Dict[str, Any]):
        """Aggiunge la sezione metriche"""
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 15, '[REPORT] Metriche Performance', 0, 1, 'L')
        
        metrics = data.get('metrics', {})
        
        # Tabella metriche
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.set_fill_color(240, 240, 240)
        
        # Header tabella
        self.pdf.cell(80, 10, 'Metrica', 1, 0, 'C', True)
        self.pdf.cell(50, 10, 'Valore', 1, 0, 'C', True)
        self.pdf.cell(50, 10, 'Stato', 1, 1, 'C', True)
        
        # Dati metriche
        self.pdf.set_font('Arial', '', 11)
        
        metric_items = [
            ('Engagement Rate', metrics.get('engagement_rate', 'N/A')),
            ('Completion Rate', metrics.get('completion_rate', 'N/A')),
            ('Share Rate', metrics.get('share_rate', 'N/A')),
            ('Comment Rate', metrics.get('comment_rate', 'N/A')),
            ('Like Rate', metrics.get('like_rate', 'N/A'))
        ]
        
        for metric_name, value in metric_items:
            self.pdf.cell(80, 8, metric_name, 1, 0)
            self.pdf.cell(50, 8, str(value), 1, 0, 'C')
            
            # Stato basato sul valore
            if isinstance(value, (int, float)):
                if value > 5:
                    status = "[OK] Ottimo"
                    self.pdf.set_text_color(0, 128, 0)
                elif value > 2:
                    status = "[WARN] Buono"
                    self.pdf.set_text_color(255, 165, 0)
                else:
                    status = "[ERROR] Migliorabile"
                    self.pdf.set_text_color(255, 0, 0)
            else:
                status = "[INFO] N/A"
                self.pdf.set_text_color(128, 128, 128)
            
            self.pdf.cell(50, 8, status, 1, 1, 'C')
            self.pdf.set_text_color(0)
    
    def _add_keywords_section(self, data: Dict[str, Any]):
        """Aggiunge la sezione keywords"""
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 15, '🏷️ Parole Chiave Identificate', 0, 1, 'L')
        
        keywords = data.get('keywords', [])
        
        if keywords:
            self.pdf.set_font('Arial', '', 12)
            self.pdf.set_text_color(0)
            
            for i, keyword in enumerate(keywords[:20], 1):  # Max 20 keywords
                self.pdf.cell(20, 8, f'{i}.', 0, 0)
                self.pdf.cell(0, 8, keyword, 0, 1)
        else:
            self.pdf.set_font('Arial', '', 12)
            self.pdf.set_text_color(128)
            self.pdf.cell(0, 10, 'Nessuna parola chiave identificata.', 0, 1)
        
        # Hashtag suggeriti
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.secondary_color)
        self.pdf.cell(0, 10, 'Hashtag Suggeriti:', 0, 1, 'L')
        
        suggested_hashtags = data.get('suggested_hashtags', [])
        self.pdf.set_font('Arial', '', 11)
        self.pdf.set_text_color(0)
        
        for hashtag in suggested_hashtags[:10]:  # Max 10 hashtag
            self.pdf.cell(0, 8, f'#{hashtag}', 0, 1)
    
    def _add_recommendations_section(self, data: Dict[str, Any]):
        """Aggiunge la sezione consigli"""
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 15, '💡 Consigli per il Miglioramento', 0, 1, 'L')
        
        recommendations = data.get('recommendations', [])
        
        if recommendations:
            self.pdf.set_font('Arial', '', 12)
            self.pdf.set_text_color(0)
            
            for i, rec in enumerate(recommendations, 1):
                self.pdf.set_font('Arial', 'B', 12)
                self.pdf.cell(0, 8, f'{i}. {rec.get("title", "Consiglio")}', 0, 1)
                
                self.pdf.set_font('Arial', '', 11)
                self.pdf.set_text_color(64, 64, 64)
                self.pdf.multi_cell(0, 6, rec.get('description', ''))
                self.pdf.set_text_color(0)
                self.pdf.ln(5)
        else:
            self.pdf.set_font('Arial', '', 12)
            self.pdf.set_text_color(128)
            self.pdf.cell(0, 10, 'Nessun consiglio specifico disponibile.', 0, 1)
    
    def _add_technical_section(self, data: Dict[str, Any]):
        """Aggiunge la sezione tecnica"""
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.primary_color)
        self.pdf.cell(0, 15, '[INFO] Dettagli Tecnici', 0, 1, 'L')
        
        # Informazioni tecniche
        tech_info = [
            ('Durata Video', data.get('duration', 'N/A')),
            ('Risoluzione', data.get('resolution', 'N/A')),
            ('Formato', data.get('format', 'N/A')),
            ('Modello AI', data.get('ai_model', 'N/A')),
            ('Versione TokIntel', data.get('version', 'v2.1'))
        ]
        
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.set_fill_color(240, 240, 240)
        
        # Header
        self.pdf.cell(80, 10, 'Parametro', 1, 0, 'C', True)
        self.pdf.cell(100, 10, 'Valore', 1, 1, 'C', True)
        
        # Dati
        self.pdf.set_font('Arial', '', 11)
        for param, value in tech_info:
            self.pdf.cell(80, 8, param, 1, 0)
            self.pdf.cell(100, 8, str(value), 1, 1)

def export_analysis_to_pdf(analysis_data: Dict[str, Any], output_path: str = None) -> str:
    """Funzione principale per esportare analisi in PDF"""
    
    try:
        exporter = PDFExporter()
        return exporter.create_report(analysis_data, output_path)
        
    except Exception as e:
        logger.error(f"Errore nell'esportazione PDF: {e}")
        raise

def create_sample_report() -> str:
    """Crea un report di esempio per testing"""
    
    sample_data = {
        "video_title": "Come Guadagnare su TikTok nel 2024",
        "analysis_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "overall_score": 78,
        "summary": "Video ben strutturato con buon potenziale virale. Il contenuto è informativo e coinvolgente, ma potrebbe beneficiare di un hook più forte nei primi secondi.",
        "key_points": [
            "Hook efficace ma potrebbe essere più forte",
            "Contenuto di valore per il target",
            "Call-to-action chiara e ben posizionata",
            "Audio di qualità e ben sincronizzato"
        ],
        "metrics": {
            "engagement_rate": 4.2,
            "completion_rate": 68,
            "share_rate": 2.1,
            "comment_rate": 1.8,
            "like_rate": 3.5
        },
        "keywords": ["guadagno", "tiktok", "2024", "strategia", "business", "social media"],
        "suggested_hashtags": ["#guadagnotiktok", "#business2024", "#strategia", "#socialmedia"],
        "recommendations": [
            {
                "title": "Migliora l'Hook",
                "description": "Inizia con una domanda più provocatoria o un fatto sorprendente per catturare immediatamente l'attenzione."
            },
            {
                "title": "Aggiungi Più Hashtag",
                "description": "Usa 5-8 hashtag rilevanti per aumentare la scopribilità del contenuto."
            }
        ],
        "duration": "45 secondi",
        "resolution": "1080x1920",
        "format": "MP4",
        "ai_model": "GPT-4",
        "version": "v2.1"
    }
    
    return export_analysis_to_pdf(sample_data, "sample_report.pdf")

if __name__ == "__main__":
    # Test del modulo
    try:
        output_file = create_sample_report()
        print(f"Report di esempio creato: {output_file}")
    except Exception as e:
        print(f"Errore: {e}") 