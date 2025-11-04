@echo off
echo ========================================
echo   Ask The Storytell AI - Quick Launch
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0" && C:\Users\Shrey\AppData\Local\Microsoft\WindowsApps\python3.12.exe run_server.py"

echo [2/2] Waiting for backend to initialize (30 seconds)...
timeout /t 30 /nobreak > nul

echo.
echo Starting Frontend...
start "Frontend Server" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo   Servers are starting!
echo ========================================
echo   Backend:  http://localhost:9000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:5173

echo.
echo Servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
