@echo off
REM Quick Start Script for CyberSafe Website (Windows)

echo ===============================================
echo CyberSafe - Cybersecurity Awareness Platform
echo ===============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ^✓ Python found
echo.

REM Install dependencies
echo Installing Python packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ^✗ Failed to install packages
    pause
    exit /b 1
)
echo ^✓ Packages installed successfully
echo.

REM Setup database
echo Setting up MySQL database...
python setup_database.py
if errorlevel 1 (
    echo ^✗ Database setup failed - check MySQL connection
) else (
    echo ^✓ Database setup completed
)
echo.

REM Run application
echo Starting CyberSafe application...
echo Application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
