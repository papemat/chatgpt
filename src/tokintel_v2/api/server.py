from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import json
from pathlib import Path
import sys

# Aggiungi il path del progetto
sys.path.append(str(Path(__file__).parent.parent))

from main import TokIntelCore
from analytics.dashboard import update_stats
from integrations.telegram_bot import send_video_report

app = FastAPI(title="TokIntel API", version="2.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli Pydantic
class TextAnalysisRequest(BaseModel):
    content: str
    title: str = "Text Analysis"

class AnalysisResponse(BaseModel):
    success: bool
    data: dict
    message: str

# Inizializza TokIntel core
tokintel = TokIntelCore()

@app.get("/")
async def root():
    return {"message": "TokIntel v2.1 API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.1.0"}

@app.post("/analyze/video", response_model=AnalysisResponse)
async def analyze_video(file: UploadFile = File(...)):
    """Analizza un file video"""
    try:
        # Salva il file temporaneamente
        temp_path = Path(f"temp_{file.filename}")
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Analizza il video
        result = await tokintel.process_video(str(temp_path))
        
        # Salva i risultati nel database analytics
        update_stats(result)
        
        # Invia report su Telegram (se configurato)
        try:
            telegram_data = {
                'title': result.get('video_title', 'Video Analizzato'),
                'score': result.get('overall_score', 0),
                'summary': result.get('summary', 'Nessuna sintesi disponibile'),
                'suggestion': result.get('team_recommendations', ['Nessun suggerimento'])[0] if result.get('team_recommendations') else 'Nessun suggerimento'
            }
            send_video_report(telegram_data)
        except Exception as e:
            print(f"Errore invio Telegram: {e}")
        
        # Rimuovi il file temporaneo
        temp_path.unlink()
        
        return AnalysisResponse(
            success=True,
            data=result,
            message="Video analizzato con successo"
        )
        
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analizza testo usando il team Devika"""
    try:
        from agent.devika_team import run_devika_team_analysis
        
        # Analizza il testo
        result = await run_devika_team_analysis(request.content)
        
        # Salva i risultati nel database analytics
        analytics_data = {
            'video_title': request.title,
            'overall_score': result.get('overall_score', 0),
            'sentiment': result.get('engagement_prediction', 0),
            'keywords': [rec[:20] for rec in result.get('team_recommendations', [])[:5]],
            'summary': 'Analisi testo completata'
        }
        update_stats(analytics_data)
        
        return AnalysisResponse(
            success=True,
            data=result,
            message="Testo analizzato con successo"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/top-videos")
async def get_top_videos(limit: int = 10):
    """Restituisce i video con punteggio più alto"""
    try:
        from analytics.dashboard import get_top_videos
        videos = get_top_videos(limit)
        return {
            "success": True,
            "data": [{"title": v[0], "score": v[1], "date": v[2]} for v in videos]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/sentiment-trend")
async def get_sentiment_trend():
    """Restituisce il trend sentiment"""
    try:
        from analytics.dashboard import get_sentiment_trend
        trend = get_sentiment_trend()
        return {
            "success": True,
            "data": [{"date": t[0], "sentiment": t[1]} for t in trend]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/keywords")
async def get_keywords():
    """Restituisce le parole chiave per wordcloud"""
    try:
        from analytics.dashboard import get_keywords_cloud
        keywords = get_keywords_cloud()
        return {
            "success": True,
            "data": keywords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 