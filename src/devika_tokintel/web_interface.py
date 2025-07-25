import streamlit as st
import subprocess
import sys
import os
from datetime import datetime
import json

# Configurazione pagina
st.set_page_config(
    page_title="Devika - TokIntel Assistant",
    page_icon="🤖",
    layout="wide"
)

# Titolo
st.title("🤖 Devika - TokIntel Assistant")
st.markdown("**Il tuo assistente AI per automatizzare e testare TokIntel**")

# Sidebar per selezione task
st.sidebar.header("[INFO] Task Disponibili")

# Lista task
tasks = {
    "🏥 System Health": "system_health",
    "⚙️ Test Config": "test_config", 
    "[INFO] Retry Logic": "retry_logic",
    "🤖 Test Agents": "test_agents",
    "⚡ LLM Benchmark": "benchmark_llm",
    "[REPORT] Export CSV": "export_csv",
    "[INFO] Refactor Prompt": "refactor_prompt",
    "[INFO] Auto Maintenance": "auto_maintenance",
    "🎤 Test Whisper": "test_whisper",
    "🤖 Test Ollama": "test_ollama",
    "🤗 Test HuggingFace": "test_huggingface"
}

selected_task = st.sidebar.selectbox(
    "Seleziona un task:",
    list(tasks.keys())
)

# Funzione per eseguire task
def run_task(task_name):
    try:
        # Cambia directory
        os.chdir(os.path.dirname(__file__))
        
        # Esegui comando
        result = subprocess.run(
            [sys.executable, "devika.py", task_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Task timeout (60s)", 1
    except Exception as e:
        return "", str(e), 1

# Contenuto principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"Task: {selected_task}")
    
    if st.button("[INFO] Esegui Task", type="primary"):
        with st.spinner("Eseguendo task..."):
            stdout, stderr, return_code = run_task(tasks[selected_task])
            
            # Mostra risultati
            if return_code == 0:
                st.success("[OK] Task completato con successo!")
            else:
                st.error("[ERROR] Task fallito")
            
            # Output
            if stdout:
                st.subheader("[INFO] Output:")
                st.code(stdout, language="bash")
            
            if stderr:
                st.subheader("[WARN]️ Errori:")
                st.code(stderr, language="bash")
            
            # Salva log
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "task": selected_task,
                "task_name": tasks[selected_task],
                "return_code": return_code,
                "stdout": stdout,
                "stderr": stderr
            }
            
            # Salva in session state per storico
            if "task_history" not in st.session_state:
                st.session_state.task_history = []
            
            st.session_state.task_history.append(log_data)

with col2:
    st.header("[REPORT] Statistiche")
    
    # Conta task eseguiti
    if "task_history" in st.session_state:
        total_tasks = len(st.session_state.task_history)
        successful_tasks = sum(1 for log in st.session_state.task_history if log["return_code"] == 0)
        
        st.metric("Task Totali", total_tasks)
        st.metric("Task Riusciti", successful_tasks)
        st.metric("Success Rate", f"{(successful_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "0%")
    
    st.header("[INFO] Task Rapidi")
    
    # Pulsanti per task comuni
    if st.button("🏥 Health Check", key="health_quick"):
        with st.spinner("Health check..."):
            stdout, stderr, return_code = run_task("system_health")
            if return_code == 0:
                st.success("[OK] Sistema OK!")
            else:
                st.error("[ERROR] Problemi rilevati")
    
    if st.button("⚙️ Test Config", key="config_quick"):
        with st.spinner("Test configurazione..."):
            stdout, stderr, return_code = run_task("test_config")
            if return_code == 0:
                st.success("[OK] Config OK!")
            else:
                st.error("[ERROR] Errori configurazione")

# Storico task
if "task_history" in st.session_state and st.session_state.task_history:
    st.header("[INFO] Storico Task")
    
    # Mostra ultimi 5 task
    recent_tasks = st.session_state.task_history[-5:]
    
    for i, log in enumerate(reversed(recent_tasks)):
        with st.expander(f"{log['timestamp'][:19]} - {log['task']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if log["stdout"]:
                    st.text("Output:")
                    st.code(log["stdout"][:500] + "..." if len(log["stdout"]) > 500 else log["stdout"])
            
            with col2:
                status = "[OK] Successo" if log["return_code"] == 0 else "[ERROR] Fallito"
                st.write(f"**Status:** {status}")
                st.write(f"**Task:** {log['task_name']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Devika - TokIntel Assistant v1.0</p>
    <p>🤖 Automatizza, testa e monitora il tuo progetto TokIntel</p>
</div>
""", unsafe_allow_html=True) 