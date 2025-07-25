"""
LLM Prompts Module
Centralized prompt templates for TokIntel
"""


class PromptTemplates:
    """Centralized prompt templates for TokIntel"""
    
    @staticmethod
    def build_summary_prompt(transcript: str, ocr_text: str) -> str:
        """Build the summary prompt for video analysis"""
        return f"""Analizza il seguente contenuto video TikTok:

- Trascrizione audio: {transcript}
- Testo visivo rilevato tramite OCR: {ocr_text}

Obiettivo:
1. Riassumi brevemente il contenuto in italiano
2. Indica il tema centrale del video
3. Specifica eventuali emozioni trasmesse
4. Valuta se è presente un 'hook' efficace nei primi secondi
5. Identifica il target audience
6. Suggerisci miglioramenti per aumentare l'engagement

Formato risposta:
- Tema principale: [descrizione]
- Emozioni: [lista emozioni]
- Hook: [valutazione hook]
- Target: [audience target]
- Suggerimenti: [lista miglioramenti]"""
    
    @staticmethod
    def build_engagement_analysis_prompt(transcript: str, ocr_text: str) -> str:
        """Build the engagement analysis prompt"""
        return f"""Analizza i seguenti fattori di engagement nel contenuto:

Trascrizione: {transcript}
Testo visivo: {ocr_text}

Valuta su una scala da 1 a 10:
1. Chiarezza del messaggio
2. Emozionalità del contenuto
3. Presenza di call-to-action
4. Rilevanza per il target
5. Originalità del contenuto
6. Timing e ritmo

Restituisci solo un JSON con i punteggi e una breve spiegazione per ciascuno."""
    
    @staticmethod
    def build_viral_potential_prompt(transcript: str, ocr_text: str, keywords: list) -> str:
        """Build the viral potential analysis prompt"""
        return f"""Analizza il potenziale virale del seguente contenuto TikTok:

Trascrizione: {transcript}
Testo visivo: {ocr_text}
Parole chiave target: {', '.join(keywords)}

Valuta su una scala da 1 a 10:
1. Probabilità di diventare virale
2. Rilevanza delle parole chiave
3. Emozionalità del contenuto
4. Originalità e creatività
5. Timing e attualità
6. Potenziale di condivisione

Restituisci un JSON con:
- punteggi per ogni fattore
- spiegazione dettagliata
- suggerimenti per migliorare la viralità"""
    
    @staticmethod
    def build_content_optimization_prompt(transcript: str, ocr_text: str, target_score: float) -> str:
        """Build the content optimization prompt"""
        return f"""Analizza il seguente contenuto TikTok e suggerisci ottimizzazioni:

Contenuto attuale:
- Trascrizione: {transcript}
- Testo visivo: {ocr_text}
- Punteggio target: {target_score}

Suggerisci miglioramenti specifici per:
1. Hook più efficace
2. Messaggio più chiaro
3. Emozioni più coinvolgenti
4. Call-to-action più forte
5. Timing ottimale
6. Elementi visivi migliori

Formato risposta:
- Problemi identificati: [lista]
- Suggerimenti specifici: [lista dettagliata]
- Priorità di implementazione: [ordine di importanza]"""
    
    @staticmethod
    def build_audience_analysis_prompt(transcript: str, ocr_text: str) -> str:
        """Build the audience analysis prompt"""
        return f"""Analizza il target audience del seguente contenuto TikTok:

Contenuto:
- Trascrizione: {transcript}
- Testo visivo: {ocr_text}

Identifica:
1. Età target
2. Interessi principali
3. Comportamenti online
4. Piattaforme preferite
5. Orari di attività
6. Motivazioni di consumo

Formato risposta:
- Demografia: [età, genere, localizzazione]
- Psicografia: [interessi, valori, stile di vita]
- Comportamenti: [abitudini online, preferenze]
- Suggerimenti targeting: [strategie specifiche]"""
    
    @staticmethod
    def build_trend_analysis_prompt(transcript: str, ocr_text: str, current_trends: list) -> str:
        """Build the trend analysis prompt"""
        return f"""Analizza l'allineamento del contenuto con le tendenze attuali:

Contenuto:
- Trascrizione: {transcript}
- Testo visivo: {ocr_text}

Tendenze attuali: {', '.join(current_trends)}

Valuta:
1. Allineamento con le tendenze
2. Opportunità di trendjacking
3. Rischio di saturazione
4. Timing ottimale
5. Differenziazione necessaria

Formato risposta:
- Allineamento: [punteggio 1-10]
- Opportunità: [lista specifiche]
- Rischi: [identificazione]
- Raccomandazioni: [azioni concrete]"""

class PromptManager:
    """Manager for prompt operations and logging"""
    
    def __init__(self):
        """Initialize prompt manager"""
        self.templates = PromptTemplates()
        self.prompt_history = []
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        """Get a prompt by type with logging"""
        try:
            if prompt_type == "summary":
                prompt = self.templates.build_summary_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", "")
                )
            elif prompt_type == "engagement":
                prompt = self.templates.build_engagement_analysis_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", "")
                )
            elif prompt_type == "viral":
                prompt = self.templates.build_viral_potential_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", ""),
                    kwargs.get("keywords", [])
                )
            elif prompt_type == "optimization":
                prompt = self.templates.build_content_optimization_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", ""),
                    kwargs.get("target_score", 0.0)
                )
            elif prompt_type == "audience":
                prompt = self.templates.build_audience_analysis_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", "")
                )
            elif prompt_type == "trend":
                prompt = self.templates.build_trend_analysis_prompt(
                    kwargs.get("transcript", ""),
                    kwargs.get("ocr_text", ""),
                    kwargs.get("current_trends", [])
                )
            else:
                raise ValueError(f"Unknown prompt type: {prompt_type}")
            
            # Log prompt usage
            self.prompt_history.append({
                "type": prompt_type,
                "timestamp": "now",  # Would use datetime in real implementation
                "kwargs": kwargs
            })
            
            return prompt
            
        except Exception as e:
            raise ValueError(f"Error generating prompt {prompt_type}: {e}")
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """Get statistics about prompt usage"""
        stats = {}
        for entry in self.prompt_history:
            prompt_type = entry["type"]
            if prompt_type not in stats:
                stats[prompt_type] = 0
            stats[prompt_type] += 1
        
        return {
            "total_prompts": len(self.prompt_history),
            "by_type": stats
        } 