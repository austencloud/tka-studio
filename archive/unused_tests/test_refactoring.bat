@echo off
REM Windows batch file to test the refactoring
REM This tries different Python commands until one works

echo 🧪 Testing refactoring with different Python commands...
echo.

REM Try py command first (Windows Python Launcher)
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Using 'py' command
    py test_refactoring.py
    goto :end
)

REM Try python3 command
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Using 'python3' command
    python3 test_refactoring.py
    goto :end
)

REM Try python command
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Using 'python' command
    python test_refactoring.py
    goto :end
)

REM Try full path to Python
if exist "C:\Users\Austen\AppData\Local\Programs\Python\Python313\python.exe" (
    echo ✅ Using full Python path
    "C:\Users\Austen\AppData\Local\Programs\Python\Python313\python.exe" test_refactoring.py
    goto :end
)

echo ❌ No Python interpreter found!
echo Please install Python or check your PATH environment variable.
echo.
echo You can try:
echo   - Install Python from python.org
echo   - Use Windows Store Python
echo   - Check your PATH environment variable

:end
pause
