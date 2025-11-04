@echo off
cls
echo ========================================
echo   Starting Ask The Storytell AI
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "C:\Users\Shrey\AppData\Local\Microsoft\WindowsApps\python3.12.exe run_server.py"

echo [2/2] Waiting 15 seconds for backend...
timeout /t 15 /nobreak >nul

echo Starting Frontend...
cd frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo   Both servers are starting!
echo ========================================
echo   Backend:  http://localhost:9000
echo   Frontend: http://localhost:5173
echo ========================================
echo.

timeout /t 5 /nobreak >nul
start http://localhost:5173

echo Press any key to exit...
pause >nul
