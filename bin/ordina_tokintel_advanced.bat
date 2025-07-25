@echo off
setlocal enabledelayedexpansion

REM ========================================
REM TokIntel Advanced File Organizer v2.0
REM ========================================

REM Configurazione
set "DESKTOP=%USERPROFILE%\Desktop"
set "WORKSPACE=%DESKTOP%\TokIntel_v2_workspace"
set "BACKUP_DIR=%DESKTOP%\TokIntel_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%"
set "LOG_FILE=%DESKTOP%\tokintel_organize.log"

REM Rimuovi spazi dal nome backup
set "BACKUP_DIR=%BACKUP_DIR: =0%"

echo ========================================
echo TokIntel Advanced File Organizer v2.0
echo ========================================
echo.
echo Desktop: %DESKTOP%
echo Workspace: %WORKSPACE%
echo Backup: %BACKUP_DIR%
echo Log: %LOG_FILE%
echo.

REM Menu principale
:menu
echo Scegli un'opzione:
echo 1. Organizza file (con backup)
echo 2. Organizza file (senza backup)
echo 3. Ripristina da backup
echo 4. Mostra log
echo 5. Esci
echo.
set /p choice="Inserisci la tua scelta (1-5): "

if "%choice%"=="1" goto organize_with_backup
if "%choice%"=="2" goto organize_no_backup
if "%choice%"=="3" goto restore_backup
if "%choice%"=="4" goto show_log
if "%choice%"=="5" goto exit
echo Scelta non valida. Riprova.
goto menu

REM ========================================
REM ORGANIZZA CON BACKUP
REM ========================================
:organize_with_backup
echo.
echo [INFO] Creazione backup...
mkdir "%BACKUP_DIR%"
echo %date% %time% - Backup creato: %BACKUP_DIR% >> "%LOG_FILE%"

REM Backup file esistenti
for %%F in (extensions tokintel_v2 results __pycache__ .venv .pytest_cache devika_tokintel tests) do (
    if exist "%DESKTOP%\%%F" (
        echo [BACKUP] Copiando %%F...
        xcopy "%DESKTOP%\%%F" "%BACKUP_DIR%\%%F" /E /I /Y >nul
        echo %date% %time% - Backup: %%F >> "%LOG_FILE%"
    )
)

REM Backup file specifici
for %%F in (%DESKTOP%\*.md %DESKTOP%\*.yml %DESKTOP%\*.json %DESKTOP%\*.bat %DESKTOP%\*.sh %DESKTOP%\*.zip %DESKTOP%\*.png %DESKTOP%\*.jpg) do (
    if exist "%%F" (
        echo [BACKUP] Copiando %%~nxF...
        copy "%%F" "%BACKUP_DIR%\" >nul
        echo %date% %time% - Backup: %%~nxF >> "%LOG_FILE%"
    )
)

echo [OK] Backup completato in: %BACKUP_DIR%
echo %date% %time% - Backup completato >> "%LOG_FILE%"
goto organize_files

REM ========================================
REM ORGANIZZA SENZA BACKUP
REM ========================================
:organize_no_backup
echo.
echo [WARN] Nessun backup verrà creato!
set /p confirm="Sei sicuro? (y/N): "
if /i not "%confirm%"=="y" goto menu
echo %date% %time% - Organizzazione senza backup >> "%LOG_FILE%"
goto organize_files

REM ========================================
REM ORGANIZZA FILE
REM ========================================
:organize_files
echo.
echo [INFO] Inizializzazione organizzazione...

REM Crea cartelle principali
echo [CREATE] Creando struttura cartelle...
mkdir "%WORKSPACE%" 2>nul
mkdir "%WORKSPACE%\src" 2>nul
mkdir "%WORKSPACE%\src\ui" 2>nul
mkdir "%WORKSPACE%\docs" 2>nul
mkdir "%WORKSPACE%\config" 2>nul
mkdir "%WORKSPACE%\bin" 2>nul
mkdir "%WORKSPACE%\assets" 2>nul
echo %date% %time% - Struttura cartelle creata >> "%LOG_FILE%"

REM Sposta cartelle principali TokIntel
echo [MOVE] Spostando cartelle principali...
for %%F in (extensions tokintel_v2 results __pycache__ .venv .pytest_cache devika_tokintel tests) do (
    if exist "%DESKTOP%\%%F" (
        echo   [MOVE] %%F → src\
        move "%DESKTOP%\%%F" "%WORKSPACE%\src\" >nul
        if !errorlevel! equ 0 (
            echo %date% %time% - Spostato: %%F → src\ >> "%LOG_FILE%"
        ) else (
            echo %date% %time% - ERRORE spostando: %%F >> "%LOG_FILE%"
        )
    )
)

REM Sposta file UI specifici
if exist "%DESKTOP%\streamlit_launcher.py" (
    echo   [MOVE] streamlit_launcher.py → src\ui\
    move "%DESKTOP%\streamlit_launcher.py" "%WORKSPACE%\src\ui\" >nul
    echo %date% %time% - Spostato: streamlit_launcher.py → src\ui\ >> "%LOG_FILE%"
)

REM Sposta file markdown
echo [MOVE] Spostando documentazione...
for %%F in (%DESKTOP%\*.md) do (
    if exist "%%F" (
        echo   [MOVE] %%~nxF → docs\
        move "%%F" "%WORKSPACE%\docs\" >nul
        if !errorlevel! equ 0 (
            echo %date% %time% - Spostato: %%~nxF → docs\ >> "%LOG_FILE%"
        ) else (
            echo %date% %time% - ERRORE spostando: %%~nxF >> "%LOG_FILE%"
        )
    )
)

REM Sposta file di configurazione
echo [MOVE] Spostando configurazioni...
for %%F in (%DESKTOP%\*.yml %DESKTOP%\*.json %DESKTOP%\launch_* %DESKTOP%\setup.py %DESKTOP%\requirements.txt) do (
    if exist "%%F" (
        echo   [MOVE] %%~nxF → config\
        move "%%F" "%WORKSPACE%\config\" >nul
        if !errorlevel! equ 0 (
            echo %date% %time% - Spostato: %%~nxF → config\ >> "%LOG_FILE%"
        ) else (
            echo %date% %time% - ERRORE spostando: %%~nxF >> "%LOG_FILE%"
        )
    )
)

REM Sposta script batch e shell
echo [MOVE] Spostando script...
for %%F in (%DESKTOP%\*.bat %DESKTOP%\*.sh) do (
    if exist "%%F" (
        echo   [MOVE] %%~nxF → bin\
        move "%%F" "%WORKSPACE%\bin\" >nul
        if !errorlevel! equ 0 (
            echo %date% %time% - Spostato: %%~nxF → bin\ >> "%LOG_FILE%"
        ) else (
            echo %date% %time% - ERRORE spostando: %%~nxF >> "%LOG_FILE%"
        )
    )
)

REM Sposta asset (zip, immagini)
echo [MOVE] Spostando asset...
for %%F in (%DESKTOP%\*.zip %DESKTOP%\*.png %DESKTOP%\*.jpg) do (
    if exist "%%F" (
        echo   [MOVE] %%~nxF → assets\
        move "%%F" "%WORKSPACE%\assets\" >nul
        if !errorlevel! equ 0 (
            echo %date% %time% - Spostato: %%~nxF → assets\ >> "%LOG_FILE%"
        ) else (
            echo %date% %time% - ERRORE spostando: %%~nxF >> "%LOG_FILE%"
        )
    )
)

echo.
echo ========================================
echo ✅ ORGANIZZAZIONE COMPLETATA!
echo ========================================
echo Workspace: %WORKSPACE%
if exist "%BACKUP_DIR%" echo Backup: %BACKUP_DIR%
echo Log: %LOG_FILE%
echo.
echo %date% %time% - Organizzazione completata >> "%LOG_FILE%"

REM Mostra statistiche
echo [STATS] Statistiche:
dir "%WORKSPACE%" /s | find "File(s)" >nul
echo.
pause
goto menu

REM ========================================
REM RIPRISTINA DA BACKUP
REM ========================================
:restore_backup
echo.
echo [INFO] Backup disponibili:
dir "%DESKTOP%\TokIntel_backup_*" /B 2>nul
if errorlevel 1 (
    echo [WARN] Nessun backup trovato!
    pause
    goto menu
)

set /p backup_name="Inserisci il nome del backup da ripristinare: "
if not exist "%DESKTOP%\%backup_name%" (
    echo [ERROR] Backup non trovato!
    pause
    goto menu
)

echo [WARN] Questo sovrascriverà i file esistenti!
set /p confirm="Sei sicuro? (y/N): "
if /i not "%confirm%"=="y" goto menu

echo [RESTORE] Ripristinando da %backup_name%...
xcopy "%DESKTOP%\%backup_name%\*" "%DESKTOP%\" /E /I /Y >nul
echo %date% %time% - Ripristinato da: %backup_name% >> "%LOG_FILE%"
echo [OK] Ripristino completato!
pause
goto menu

REM ========================================
REM MOSTRA LOG
REM ========================================
:show_log
echo.
echo [LOG] Ultimi 20 eventi:
if exist "%LOG_FILE%" (
    powershell "Get-Content '%LOG_FILE%' | Select-Object -Last 20"
) else (
    echo [INFO] Nessun log trovato.
)
echo.
pause
goto menu

REM ========================================
REM USCITA
REM ========================================
:exit
echo.
echo Grazie per aver usato TokIntel Advanced File Organizer!
echo.
pause
exit /b 0 