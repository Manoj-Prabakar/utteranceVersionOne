@echo off
echo ========================================
echo   Utterance Intention Generator
echo   Using Google ADK and Gemini Flash
echo ========================================
echo.

REM Check if requirements are installed
echo Checking dependencies...
pip show google-adk >nul 2>&1
if errorlevel 1 (
    echo Installing google-adk...
    pip install google-adk>=1.2.1
)

echo.
echo Starting Utterance Generator...
echo.

REM Run the main script
python main.py

echo.
echo Press any key to exit...
pause >nul