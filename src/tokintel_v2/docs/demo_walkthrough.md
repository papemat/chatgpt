# [INFO] TokIntel v2 – Demo Walkthrough

## 1. Analisi da linea di comando (CLI)
```bash
tokintel analyze media/demo_video.mp4
```
Output: verrà generato un file JSON con punteggi, parole chiave, engagement e sintesi automatica.

## 2. Interfaccia utente (UI Streamlit)
```bash
streamlit run ui/interface.py
```
Questo comando avvia l’interfaccia interattiva. Accedi su http://localhost:8501.

## 3. Esecuzione via Docker
```bash
docker-compose up
```
Assicurati di avere Docker installato. Questo comando lancia UI e CLI in contenitori separati.

## 4. Colab Notebook (da browser)
Vai al link: TokIntel_Colab_Demo.ipynb

## 5. [Facoltativo] Registrare demo video
Puoi usare strumenti come OBS Studio o Peek per creare una demo visiva di 30–60 sec da allegare al README o su YouTube. 