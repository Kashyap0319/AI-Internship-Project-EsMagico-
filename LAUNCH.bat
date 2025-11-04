@echo off
cls
echo ============================================================
echo   Ask The Storytell AI - LAUNCHER
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend...
start "Storytell Backend" cmd /k "python run_server.py"

echo [2/2] Waiting 10 seconds for backend...
timeout /t 10 /nobreak >nul

echo Starting Frontend...
cd frontend
start "Storytell Frontend" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo   SERVERS RUNNING!
echo ============================================================
echo   Backend:  http://localhost:9000/docs
echo   Frontend: http://localhost:5173
echo ============================================================
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

exit
