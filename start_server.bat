@echo off
echo Starting OralAI Backend Server...
echo Access the application at http://localhost:8000

:: Check if venv exists and create it if necessary
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Upgrade build tools
echo Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

:: Install requirements
echo Checking and installing required libraries...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install requirements.
    echo Please check your internet connection or python compatibility.
    pause
    exit /b %errorlevel%
)

:: Open browser after 5 seconds
start "" cmd /c "timeout /t 5 >nul & start http://localhost:8000"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause