@echo off
REM TokIntel v2 - TikTok Integration Setup Script for Windows

echo 🎵 TokIntel v2 - Setup Integrazione TikTok
echo ==========================================

REM Verifica Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non trovato. Installa Python 3.8+ prima di continuare.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% trovato

REM Verifica pip
echo [INFO] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip non trovato. Installa pip prima di continuare.
    pause
    exit /b 1
)

echo [SUCCESS] pip trovato

REM Installa dipendenze Python
echo [INFO] Installando dipendenze Python...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Errore nell'installazione delle dipendenze Python
    pause
    exit /b 1
)

echo [SUCCESS] Dipendenze Python installate

REM Installa Playwright
echo [INFO] Installando Playwright...
python -m playwright install chromium

if errorlevel 1 (
    echo [ERROR] Errore nell'installazione di Playwright
    pause
    exit /b 1
)

echo [SUCCESS] Playwright installato

REM Installa dipendenze di sistema per Playwright
echo [INFO] Installando dipendenze di sistema per Playwright...
python -m playwright install-deps

if errorlevel 1 (
    echo [WARNING] Alcune dipendenze di sistema potrebbero non essere installate correttamente
) else (
    echo [SUCCESS] Dipendenze di sistema installate
)

REM Crea directory necessarie
echo [INFO] Creando directory necessarie...
if not exist "config" mkdir config
if not exist "logs" mkdir logs
if not exist "output" mkdir output

echo [SUCCESS] Directory create

REM Crea file di configurazione se non esiste
if not exist "config\config.yaml" (
    echo [INFO] Creando file di configurazione...
    copy config.yaml.example config\config.yaml >nul
    echo [SUCCESS] File di configurazione creato
    echo [WARNING] Modifica config\config.yaml con le tue credenziali TikTok
) else (
    echo [INFO] File di configurazione già esistente
)

REM Verifica installazione
echo [INFO] Verificando installazione...

REM Test import moduli
python -c "import playwright; print('✓ Playwright importato correttamente')"
if errorlevel 1 (
    echo [ERROR] Errore import Playwright
    pause
    exit /b 1
)

python -c "import cryptography; print('✓ Cryptography importato correttamente')"
if errorlevel 1 (
    echo [ERROR] Errore import Cryptography
    pause
    exit /b 1
)

python -c "import yaml; print('✓ PyYAML importato correttamente')"
if errorlevel 1 (
    echo [ERROR] Errore import PyYAML
    pause
    exit /b 1
)

echo ✓ Tutti i moduli importati correttamente
echo [SUCCESS] Verifica installazione completata

REM Test Playwright browser
echo [INFO] Testando browser Playwright...
python -c "
import asyncio
from playwright.async_api import async_playwright

async def test_browser():
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.tiktok.com')
        await browser.close()
        await playwright.stop()
        print('✓ Browser Playwright funzionante')
    except Exception as e:
        print(f'✗ Errore browser Playwright: {e}')
        exit(1)

asyncio.run(test_browser())
"

if errorlevel 1 (
    echo [ERROR] Errore nel test browser
    pause
    exit /b 1
)

echo [SUCCESS] Test browser completato

REM Mostra istruzioni finali
echo.
echo 🎉 Setup completato con successo!
echo ================================
echo.
echo 📋 Prossimi passi:
echo.
echo 1. 📝 Configura le credenziali TikTok:
echo    - Vai su https://developers.tiktok.com/
echo    - Crea una nuova app
echo    - Modifica config\config.yaml con le tue credenziali
echo.
echo 2. 🚀 Avvia l'interfaccia TikTok:
echo    streamlit run ui\import_tiktok.py
echo.
echo 3. 📚 Leggi la documentazione:
echo    type TIKTOK_INTEGRATION.md
echo.
echo 4. 🔧 Configurazione avanzata:
echo    - Modifica config\config.yaml per personalizzare
echo    - Controlla logs\ per debugging
echo.
echo ⚠️  Note importanti:
echo    - Rispetta i Terms of Service di TikTok
echo    - Usa solo le API ufficiali
echo    - Non condividere le tue credenziali
echo.
echo 📞 Supporto:
echo    - GitHub Issues: https://github.com/your-repo/issues
echo    - Documentazione: TIKTOK_INTEGRATION.md
echo.

echo [SUCCESS] Setup completato! 🎵
pause 