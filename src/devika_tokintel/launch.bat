@echo off
chcp 65001 >nul
title Devika TokIntel - Enhanced AI Integration System

:: Set colors for better UI
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RED=[91m"
set "CYAN=[96m"
set "WHITE=[97m"
set "RESET=[0m"

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python not found! Please install Python 3.8+ and add it to PATH.%RESET%
    echo.
    echo %YELLOW%💡 Download Python from: https://www.python.org/downloads/%RESET%
    pause
    exit /b 1
)

:: Display header
echo.
echo %CYAN%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %CYAN%║                    Devika TokIntel                          ║%RESET%
echo %CYAN%║              Enhanced AI Integration System                  ║%RESET%
echo %CYAN%║              with Automatic Model Management                 ║%RESET%
echo %CYAN%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.

:: Check if setup has been run
if not exist "logs\setup_report.json" (
    echo %YELLOW%⚠️  First time setup detected!%RESET%
    echo %WHITE%Running initial setup...%RESET%
    echo.
    python setup.py
    if errorlevel 1 (
        echo %RED%❌ Setup failed! Please check the logs and try again.%RESET%
        pause
        exit /b 1
    )
    echo.
)

:MAIN_MENU
cls
echo %CYAN%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %CYAN%║                    Devika TokIntel                          ║%RESET%
echo %CYAN%║              Enhanced AI Integration System                  ║%RESET%
echo %CYAN%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.
echo %WHITE%🚀 Quick Start Options:%RESET%
echo.
echo %GREEN%1.%RESET% %WHITE%Test Model Management%RESET%     %YELLOW%[Check LLM models status]%RESET%
echo %GREEN%2.%RESET% %WHITE%System Health Check%RESET%       %YELLOW%[Full system diagnostics]%RESET%
echo %GREEN%3.%RESET% %WHITE%LLM Benchmark%RESET%            %YELLOW%[Performance comparison]%RESET%
echo %GREEN%4.%RESET% %WHITE%Web Interface%RESET%            %YELLOW%[Streamlit GUI]%RESET%
echo.
echo %WHITE%🔧 Advanced Options:%RESET%
echo.
echo %GREEN%5.%RESET% %WHITE%Test LM Studio%RESET%           %YELLOW%[LM Studio integration]%RESET%
echo %GREEN%6.%RESET% %WHITE%Test Ollama%RESET%              %YELLOW%[Ollama integration]%RESET%
echo %GREEN%7.%RESET% %WHITE%Test HuggingFace%RESET%         %YELLOW%[NLP tasks]%RESET%
echo %GREEN%8.%RESET% %WHITE%Test Whisper%RESET%             %YELLOW%[Audio transcription]%RESET%
echo.
echo %WHITE%🛠️  Maintenance:%RESET%
echo.
echo %GREEN%9.%RESET% %WHITE%Run Setup%RESET%                %YELLOW%[Reinstall dependencies]%RESET%
echo %GREEN%10.%RESET% %WHITE%List All Tasks%RESET%           %YELLOW%[Show available commands]%RESET%
echo %GREEN%11.%RESET% %WHITE%Open Logs Directory%RESET%      %YELLOW%[View logs and reports]%RESET%
echo.
echo %GREEN%0.%RESET% %WHITE%Exit%RESET%
echo.
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.

set /p "choice=%WHITE%Select an option (0-11): %RESET%"

if "%choice%"=="1" goto TEST_MODEL_MANAGEMENT
if "%choice%"=="2" goto SYSTEM_HEALTH
if "%choice%"=="3" goto BENCHMARK_LLM
if "%choice%"=="4" goto WEB_INTERFACE
if "%choice%"=="5" goto TEST_LMSTUDIO
if "%choice%"=="6" goto TEST_OLLAMA
if "%choice%"=="7" goto TEST_HUGGINGFACE
if "%choice%"=="8" goto TEST_WHISPER
if "%choice%"=="9" goto RUN_SETUP
if "%choice%"=="10" goto LIST_TASKS
if "%choice%"=="11" goto OPEN_LOGS
if "%choice%"=="0" goto EXIT

echo %RED%Invalid option! Please select 0-11.%RESET%
timeout /t 2 >nul
goto MAIN_MENU

:TEST_MODEL_MANAGEMENT
echo.
echo %CYAN%🔧 Testing Automatic Model Management...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py test_model_management
echo.
echo %GREEN%✅ Model management test completed!%RESET%
echo %YELLOW%💡 Check the output above for model status and download instructions.%RESET%
pause
goto MAIN_MENU

:SYSTEM_HEALTH
echo.
echo %CYAN%🏥 Running System Health Check...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py system_health
echo.
echo %GREEN%✅ System health check completed!%RESET%
echo %YELLOW%💡 Check the logs directory for detailed reports.%RESET%
pause
goto MAIN_MENU

:BENCHMARK_LLM
echo.
echo %CYAN%⚡ Running LLM Benchmark...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py benchmark_llm
echo.
echo %GREEN%✅ LLM benchmark completed!%RESET%
echo %YELLOW%💡 Check the benchmark results above for performance comparison.%RESET%
pause
goto MAIN_MENU

:WEB_INTERFACE
echo.
echo %CYAN%🌐 Starting Web Interface...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
echo %WHITE%Starting Streamlit web interface...%RESET%
echo %YELLOW%💡 The web interface will open in your browser at http://localhost:8501%RESET%
echo %YELLOW%💡 Press Ctrl+C to stop the web interface%RESET%
echo.
streamlit run web_interface.py
echo.
echo %GREEN%✅ Web interface stopped.%RESET%
pause
goto MAIN_MENU

:TEST_LMSTUDIO
echo.
echo %CYAN%🤖 Testing LM Studio Integration...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py test_lmstudio
echo.
echo %GREEN%✅ LM Studio test completed!%RESET%
pause
goto MAIN_MENU

:TEST_OLLAMA
echo.
echo %CYAN%🐙 Testing Ollama Integration...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py test_ollama
echo.
echo %GREEN%✅ Ollama test completed!%RESET%
pause
goto MAIN_MENU

:TEST_HUGGINGFACE
echo.
echo %CYAN%🤗 Testing HuggingFace Integration...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py test_huggingface
echo.
echo %GREEN%✅ HuggingFace test completed!%RESET%
pause
goto MAIN_MENU

:TEST_WHISPER
echo.
echo %CYAN%🎤 Testing Whisper Integration...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py test_whisper
echo.
echo %GREEN%✅ Whisper test completed!%RESET%
pause
goto MAIN_MENU

:RUN_SETUP
echo.
echo %CYAN%🔧 Running Setup...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
echo %YELLOW%⚠️  This will reinstall dependencies and check system configuration.%RESET%
set /p "confirm=%WHITE%Continue? (y/N): %RESET%"
if /i "%confirm%"=="y" (
    python setup.py
    echo.
    echo %GREEN%✅ Setup completed!%RESET%
) else (
    echo %YELLOW%Setup cancelled.%RESET%
)
pause
goto MAIN_MENU

:LIST_TASKS
echo.
echo %CYAN%📋 Available Tasks:%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
python devika.py
echo.
echo %YELLOW%💡 Use 'python devika.py <task_name>' to run any task directly.%RESET%
pause
goto MAIN_MENU

:OPEN_LOGS
echo.
echo %CYAN%📁 Opening Logs Directory...%RESET%
echo %CYAN%══════════════════════════════════════════════════════════════════%RESET%
echo.
if exist "logs" (
    explorer "logs"
    echo %GREEN%✅ Logs directory opened!%RESET%
) else (
    echo %YELLOW%⚠️  Logs directory not found. Run a task first to generate logs.%RESET%
)
pause
goto MAIN_MENU

:EXIT
echo.
echo %CYAN%👋 Thank you for using Devika TokIntel!%RESET%
echo %WHITE%🚀 Enhanced AI Integration System with Automatic Model Management%RESET%
echo.
echo %YELLOW%💡 Quick reference:%RESET%
echo %WHITE%   • Test models: python devika.py test_model_management%RESET%
echo %WHITE%   • System health: python devika.py system_health%RESET%
echo %WHITE%   • Benchmark: python devika.py benchmark_llm%RESET%
echo %WHITE%   • Web interface: streamlit run web_interface.py%RESET%
echo.
echo %GREEN%✅ Goodbye!%RESET%
timeout /t 3 >nul
exit /b 0 