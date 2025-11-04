@echo off
echo ============================================================
echo SIMPLE BACKEND START - DETAILED ERRORS
echo ============================================================
echo.

cd /d "%~dp0"

python -c "print('Python is working'); import sys; print(f'Python version: {sys.version}')"
echo.

echo Starting uvicorn...
python -m uvicorn backend:app --host 127.0.0.1 --port 9000 --log-level info

pause
