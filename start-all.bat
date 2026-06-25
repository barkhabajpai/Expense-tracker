@echo off
REM Quick Start Script for Expense Tracker with ML

echo.
echo ========================================
echo Expense Tracker with Auto-Categorization
echo ========================================
echo.
echo Starting services...
echo.

REM Start ML Server
echo Starting ML Server on port 5001...
start "ML Server" cmd /k "cd /d "%cd%" && python ml_server.py"
timeout /t 2 >nul

REM Start Express Backend
echo Starting Express Backend on port 5000...
start "Express Backend" cmd /k "cd /d "%cd%" && npm run server"
timeout /t 2 >nul

REM Start React Frontend
echo Starting React Frontend on port 3000...
start "React Frontend" cmd /k "cd /d "%cd%" && npm start"

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Frontend:    http://localhost:3000
echo Backend:     http://localhost:5000
echo ML Server:   http://localhost:5001
echo.
echo Close any terminal window to stop that service
echo.
pause
