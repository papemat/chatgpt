@echo off
setlocal enabledelayedexpansion

REM Percorso Desktop
set "DESKTOP=%USERPROFILE%\Desktop"
set "WORKSPACE=%DESKTOP%\TokIntel_v2_workspace"

REM Crea cartelle principali
mkdir "%WORKSPACE%\src"
mkdir "%WORKSPACE%\src\ui"
mkdir "%WORKSPACE%\docs"
mkdir "%WORKSPACE%\config"
mkdir "%WORKSPACE%\bin"
mkdir "%WORKSPACE%\assets"

REM Sposta cartelle principali TokIntel
for %%F in (extensions tokintel_v2 results __pycache__ .venv .pytest_cache devika_tokintel tests) do (
    if exist "%DESKTOP%\%%F" move "%DESKTOP%\%%F" "%WORKSPACE%\src\"
)

REM Sposta file UI specifici
if exist "%DESKTOP%\streamlit_launcher.py" move "%DESKTOP%\streamlit_launcher.py" "%WORKSPACE%\src\ui\"

REM Sposta file markdown
for %%F in (%DESKTOP%\*.md) do (
    if exist "%%F" move "%%F" "%WORKSPACE%\docs\"
)

REM Sposta file di configurazione
for %%F in (%DESKTOP%\*.yml %DESKTOP%\*.json %DESKTOP%\launch_* %DESKTOP%\setup.py %DESKTOP%\requirements.txt) do (
    if exist "%%F" move "%%F" "%WORKSPACE%\config\"
)

REM Sposta script batch e shell
for %%F in (%DESKTOP%\*.bat %DESKTOP%\*.sh) do (
    if exist "%%F" move "%%F" "%WORKSPACE%\bin\"
)

REM Sposta asset (zip, immagini)
for %%F in (%DESKTOP%\*.zip %DESKTOP%\*.png %DESKTOP%\*.jpg) do (
    if exist "%%F" move "%%F" "%WORKSPACE%\assets\"
)

echo.
echo ✅ Tutti i file TokIntel sono stati ordinati in TokIntel_v2_workspace!
pause 