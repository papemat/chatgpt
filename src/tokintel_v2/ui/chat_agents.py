"""
💬 Chat Interattiva con Agenti AI - TokIntel v2.1
Sistema di conversazione con agenti specializzati per analisi TikTok
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentChat:
    """Sistema di chat con agenti AI specializzati"""
    
    def __init__(self):
        self.agents = {
            "strategist": {
                "name": "[STRATEGIST]",
                "role": "Esperto di strategia TikTok e crescita organica",
                "avatar": "[STRATEGIST]",
                "expertise": ["algoritmi", "trending", "hashtag", "timing", "engagement"]
            },
            "copywriter": {
                "name": "[COPYWRITER]", 
                "role": "Specialista in copywriting e storytelling",
                "avatar": "[COPYWRITER]",
                "expertise": ["hook", "call-to-action", "narrativa", "emozioni", "branding"]
            },
            "analyst": {
                "name": "[ANALYST]",
                "role": "Analista dati e metriche performance",
                "avatar": "[ANALYST]", 
                "expertise": ["metriche", "analisi", "benchmark", "ottimizzazione", "ROI"]
            }
        }
    
    def get_agent_response(self, agent_id: str, message: str, context: Optional[Dict] = None) -> str:
        """Simula la risposta di un agente specifico"""
        
        agent = self.agents[agent_id]
        
        # Logica di risposta basata sull'agente
        if agent_id == "strategist":
            return self._strategist_response(message, context)
        elif agent_id == "copywriter":
            return self._copywriter_response(message, context)
        elif agent_id == "analyst":
            return self._analyst_response(message, context)
        
        return "Mi dispiace, non ho capito la richiesta."
    
    def _strategist_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Risposta dello Strategist"""
        responses = [
            "[STRATEGIST] Dal punto di vista strategico, ti consiglio di focalizzarti sui trend emergenti. L'algoritmo TikTok premia i contenuti che seguono le tendenze attuali.",
            "[INFO] Per massimizzare la visibilità, pubblica nei momenti di picco di attività del tuo target (solitamente 19-22).",
            "[TAG] Usa hashtag specifici ma non troppo popolari. Mixa hashtag di nicchia con quelli trending.",
            "[TIME] La frequenza ideale è 1-2 post al giorno. La consistenza è più importante della quantità.",
            "[TIP] Crea contenuti che incoraggino l'interazione: domande, challenge, duetti."
        ]
        return responses[hash(message) % len(responses)]
    
    def _copywriter_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Risposta del Copywriter"""
        responses = [
            "[COPYWRITER] Il tuo hook deve catturare l'attenzione nei primi 3 secondi. Usa domande provocatorie o fatti sorprendenti.",
            "[INFO] Il copy deve essere conversazionale e autentico. Parla come parleresti a un amico.",
            "[STORY] Racconta una storia. Le persone si connettono con le narrazioni personali.",
            "[EMOZIONE] Usa emozioni forti: curiosità, sorpresa, ispirazione, divertimento.",
            "[CALL] Includi sempre una call-to-action chiara: 'Salva questo video', 'Segui per più consigli'."
        ]
        return responses[hash(message) % len(responses)]
    
    def _analyst_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Risposta dell'Analyst"""
        responses = [
            "[ANALYST] I dati mostrano che i video sotto i 60 secondi hanno il 40% in più di engagement.",
            "[INFO] Il completion rate è il KPI più importante. Mira al 70%+ per contenuti virali.",
            "[STRATEGIST] L'algoritmo premia la retention. I primi 3 secondi sono cruciali per mantenere l'attenzione.",
            "[INFO] I contenuti verticali (9:16) performano meglio del 15% rispetto ai formati orizzontali.",
            "[TIME] Il sweet spot per la durata è 15-30 secondi per massimizzare la distribuzione."
        ]
        return responses[hash(message) % len(responses)]

def render_chat_interface():
    """Rende l'interfaccia di chat principale"""
    
    st.title("💬 Chat con Agenti AI - TokIntel")
    st.markdown("Parla con i nostri esperti AI per consigli su TikTok!")
    
    # Inizializza la chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = "strategist"
    
    # Sidebar per selezione agente
    with st.sidebar:
        st.header("🤖 Seleziona Agente")
        
        agent_chat = AgentChat()
        
        for agent_id, agent_info in agent_chat.agents.items():
            if st.button(f"{agent_info['avatar']} {agent_info['name']}", key=f"agent_{agent_id}"):
                st.session_state.selected_agent = agent_id
        
        # Mostra info agente selezionato
        selected_agent_info = agent_chat.agents[st.session_state.selected_agent]
        st.markdown(f"**Agente attivo:** {selected_agent_info['name']}")
        st.markdown(f"**Ruolo:** {selected_agent_info['role']}")
        st.markdown("**Competenze:**")
        for skill in selected_agent_info['expertise']:
            st.markdown(f"- {skill}")
    
    # Area chat principale
    chat_container = st.container()
    
    with chat_container:
        # Mostra messaggi esistenti
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])
        
        # Input utente
        if prompt := st.chat_input("Scrivi il tuo messaggio..."):
            # Aggiungi messaggio utente
            st.session_state.chat_messages.append({
                "role": "user",
                "content": prompt,
                "avatar": "[USER]",
                "timestamp": datetime.now()
            })
            
            # Mostra messaggio utente
            with st.chat_message("user", avatar="[USER]"):
                st.markdown(prompt)
            
            # Genera risposta agente
            agent_response = agent_chat.get_agent_response(
                st.session_state.selected_agent, 
                prompt
            )
            
            # Aggiungi risposta agente
            selected_agent_info = agent_chat.agents[st.session_state.selected_agent]
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": agent_response,
                "avatar": selected_agent_info["avatar"],
                "timestamp": datetime.now()
            })
            
            # Mostra risposta agente
            with st.chat_message("assistant", avatar=selected_agent_info["avatar"]):
                st.markdown(agent_response)
    
    # Pulsanti azioni
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("[CLEAR] Cancella Chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col2:
        if st.button("💾 Salva Chat"):
            if st.session_state.chat_messages:
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "agent": st.session_state.selected_agent,
                    "messages": st.session_state.chat_messages
                }
                st.download_button(
                    label="[INFO] Scarica JSON",
                    data=json.dumps(chat_data, indent=2, default=str),
                    file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    with col3:
        if st.button("[INFO] Nuova Sessione"):
            st.session_state.chat_messages = []
            st.rerun()

def main():
    """Funzione principale per lanciare la chat"""
    st.set_page_config(
        page_title="TokIntel Chat Agents",
        page_icon="💬",
        layout="wide"
    )
    
    render_chat_interface()

if __name__ == "__main__":
    main() 