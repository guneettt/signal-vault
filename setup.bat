@echo off
echo 🚀 Setting up SignalVault Emergency Information Hub
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Found Python %python_version%

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies
echo 📚 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete! 🎉
echo.
echo To run SignalVault:
echo   1. Activate the virtual environment: .venv\Scripts\activate
echo   2. Run the application: python app.py
echo   3. Open your browser to: http://127.0.0.1:5000
echo.
echo For CLI interface: python main.py
echo.
echo Need help? Check the README.md file for detailed instructions.
pause
