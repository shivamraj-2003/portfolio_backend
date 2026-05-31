@echo off
echo Starting Portfolio Backend Server...
echo.

if not exist venv (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
