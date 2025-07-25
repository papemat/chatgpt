import streamlit as st
from typing import Dict, Any, Optional


def render_status_badge(status: str) -> None:
    """Renderizza un badge di stato colorato per il video."""
    status_map = {
        'analyzed': ('[OK] Analizzato', 'status-analyzed'),
        'new': ('[WARN] Nuovo', 'status-pending'),
        'error': ('[ERROR] Errore', 'status-error'),
    }
    label, css_class = status_map.get(status, (status, 'status-badge'))
    st.markdown(f'<span class="status-badge {css_class}">{label}</span>', unsafe_allow_html=True)


def render_video_card(video: Dict[str, Any]) -> None:
    """Renderizza una card per un singolo video con badge di stato e metadati."""
    with st.container():
        st.markdown(f"""
        <div class="video-card">
            <h4>[VIDEO] {video.get('video_title', video['video_id'][:20])}</h4>
            <p><strong>Stato:</strong> <span class="status-badge status-{video['status']}">{video['status_display']}</span></p>
            <p><strong>Creatore:</strong> {video.get('creator_username', 'N/A')}</p>
            <p><strong>Dimensione:</strong> {video['file_size_mb']} MB</p>
            <p><strong>Data:</strong> {video['download_date'].strftime('%Y-%m-%d') if video['download_date'] else 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
        if video.get('score') is not None:
            st.metric("Punteggio", f"{video['score']:.1f}/10")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("[PREVIEW] Anteprima", key=f"preview_{video['video_id']}"):
                st.session_state.preview_video = video
        with col2:
            if st.button("[REANALYZE] Rianalizza", key=f"reanalyze_{video['video_id']}"):
                st.session_state.reanalyze_video = video
        with col3:
            if st.button("[REMOVE] Rimuovi", key=f"remove_{video['video_id']}"):
                st.session_state.remove_video = video


def render_metrics(metrics: Dict[str, Any]) -> None:
    """Renderizza una riga di metriche (totali, analizzati, dimensione, punteggio medio)."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Video Totali", metrics.get('total_videos', 0))
    with col2:
        st.metric("Analizzati", metrics.get('analyzed_videos', 0))
    with col3:
        st.metric("Dimensione Totale", f"{metrics.get('total_size', 0):.1f} MB")
    with col4:
        st.metric("Punteggio Medio", f"{metrics.get('avg_score', 0):.1f}/10")


def render_progress_bar(progress: float, message: Optional[str] = None) -> None:
    """Renderizza una progress bar con messaggio opzionale."""
    bar = st.progress(progress)
    if message:
        st.write(message) 