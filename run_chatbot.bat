@echo off
echo ===============================================
echo  Setup & Configuration Chatbot
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Running Streamlit app...
echo.
echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run chatbot_app.py

pause
