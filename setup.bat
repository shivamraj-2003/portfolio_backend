@echo off
echo ========================================
echo Portfolio Backend Setup
echo ========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [5/5] Checking .env file...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please update the .env file with your credentials:
    echo    - MONGODB_URL (your MongoDB connection string)
    echo    - SECRET_KEY (generate a secure key)
    echo    - ADMIN_EMAIL & ADMIN_PASSWORD (for dashboard login)
    echo.
) else (
    echo ✓ .env file already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload
echo.
echo Or simply run: start.bat
echo.
pause
