@echo off
setlocal enabledelayedexpansion
title TrustChain-AI Launcher
color 0B

echo ============================================================
echo TRUSTCHAIN-AI
echo AI Agent Trust ^& Security Operations Center
echo ============================================================
echo.

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

cd /d "%PROJECT_ROOT%"

echo [1/4] Checking project prerequisites...
if not exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at:
    echo         "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
    echo Please ensure the Python virtual environment is set up.
    echo.
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%\frontend\package.json" (
    echo [ERROR] Frontend project not found at:
    echo         "%PROJECT_ROOT%\frontend\package.json"
    echo Please ensure the frontend directory is present.
    echo.
    pause
    exit /b 1
)
echo [OK] Project files verified.
echo.

:: Port 8050 Check & Launch
echo [2/4] Initializing Backend Service (:8050)...
netstat -ano | findstr ":8050" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] TrustChain-AI backend appears to already be running on port 8050.
) else (
    echo Starting FastAPI backend in a dedicated terminal window...
    start "TrustChain-AI Backend :8050" cmd /k "cd /d ""%PROJECT_ROOT%"" && title TrustChain-AI Backend :8050 && color 0A && call "".venv\Scripts\activate.bat"" && python -m uvicorn akta.server:app --host 0.0.0.0 --port 8050"
    echo Waiting for backend API to initialize...
    ping 127.0.0.1 -n 4 >nul 2>&1
)
echo.

:: Port 5173 Check & Launch
echo [3/4] Initializing Frontend Dashboard (:5173)...
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] TrustChain-AI frontend appears to already be running on port 5173.
) else (
    echo Starting React/Vite frontend in a dedicated terminal window...
    start "TrustChain-AI Frontend :5173" cmd /k "cd /d ""%PROJECT_ROOT%\frontend"" && title TrustChain-AI Frontend :5173 && color 03 && npm run dev"
    echo Waiting for frontend server to initialize...
    ping 127.0.0.1 -n 4 >nul 2>&1
)
echo.

echo [4/4] Opening Web Operations Center...
start http://localhost:5173

echo.
echo ============================================================
echo TRUSTCHAIN-AI READY
echo ============================================================
echo.
echo Backend:
echo   http://127.0.0.1:8050
echo.
echo Health:
echo   http://127.0.0.1:8050/health
echo.
echo Swagger Docs:
echo   http://127.0.0.1:8050/docs
echo.
echo Frontend SOC:
echo   http://localhost:5173
echo.
echo ============================================================
echo Keep the backend and frontend terminal windows open.
echo To cleanly stop the application, run STOP_TRUSTCHAIN.bat.
echo ============================================================
echo.
ping 127.0.0.1 -n 4 >nul 2>&1
