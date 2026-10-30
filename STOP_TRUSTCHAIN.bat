@echo off
setlocal enabledelayedexpansion
title TrustChain-AI Shutdown
color 0C

echo ============================================================
echo TRUSTCHAIN-AI
echo Stopping application...
echo ============================================================
echo.

set "BACKEND_STOPPED=0"
set "FRONTEND_STOPPED=0"

:: Stop Backend on Port 8050
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8050" ^| findstr "LISTENING"') do (
    set "PID_8050=%%a"
    if defined PID_8050 (
        taskkill /F /T /PID !PID_8050! >nul 2>&1
        set "BACKEND_STOPPED=1"
    )
)

if "!BACKEND_STOPPED!"=="1" (
    echo Backend  :8050 -^> stopped
) else (
    echo Backend  :8050 -^> not running
)

:: Stop Frontend on Port 5173
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do (
    set "PID_5173=%%a"
    if defined PID_5173 (
        taskkill /F /T /PID !PID_5173! >nul 2>&1
        set "FRONTEND_STOPPED=1"
    )
)

if "!FRONTEND_STOPPED!"=="1" (
    echo Frontend :5173 -^> stopped
) else (
    echo Frontend :5173 -^> not running
)

echo.
echo ============================================================
echo TrustChain-AI stopped successfully.
echo ============================================================
echo.
ping 127.0.0.1 -n 3 >nul 2>&1
