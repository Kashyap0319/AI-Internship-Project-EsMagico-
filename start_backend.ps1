# Start Backend Script
$env:PYTHONPATH = "C:\Users\Shrey\OneDrive\Desktop\Day 2 Ai Project"
Set-Location "C:\Users\Shrey\OneDrive\Desktop\Day 2 Ai Project"
Write-Host "Starting backend on port 9000..." -ForegroundColor Cyan
C:/Users/Shrey/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m uvicorn backend:app --host 0.0.0.0 --port 9000
