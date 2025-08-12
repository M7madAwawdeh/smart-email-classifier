@echo off
echo.
echo 🧠 Smart Email Classifier with AI
echo ====================================
echo.

echo 🔍 Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo 🔍 Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo 🔍 Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm not found. Please install npm
    pause
    exit /b 1
)

echo ✅ All dependencies found!
echo.

echo 🚀 Starting Smart Email Classifier...
echo.

echo 📱 Frontend will be available at: http://localhost:3000
echo 🔧 Backend will be available at: http://localhost:5000
echo.

echo Press Ctrl+C to stop all services
echo.

REM Start the Python startup script
python start.py

pause 