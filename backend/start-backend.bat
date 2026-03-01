@echo off
REM Backend startup script with auto venv activation
REM Usage: start-backend.bat [port]

setlocal enabledelayedexpansion

REM Set default port
set PORT=%1
if "%PORT%"=="" set PORT=8000

REM Change to backend directory
cd /d "%~dp0"

REM Check if venv exists, create if not
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\Lib\site-packages\uvicorn" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        exit /b 1
    )
)

REM Start the server using venv python
echo Starting FastAPI server on port %PORT%...
venv\Scripts\python.exe -m uvicorn main:app --reload --port %PORT%

endlocal
