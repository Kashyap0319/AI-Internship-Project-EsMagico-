@echo off
cd /d "C:\Users\Shrey\OneDrive\Desktop\Day 2 Ai Project"
echo Starting backend on port 9000...
echo.
C:\Users\Shrey\AppData\Local\Microsoft\WindowsApps\python3.12.exe -m uvicorn backend:app --host 0.0.0.0 --port 9000
pause
