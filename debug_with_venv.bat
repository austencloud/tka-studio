@echo off
echo 🔧 Starting TKA with Virtual Environment...
echo.

REM Set the virtual environment paths
set VIRTUAL_ENV=%~dp0.venv
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set PYTHONPATH=%VIRTUAL_ENV%\Lib\site-packages

echo ✅ Virtual Environment: %VIRTUAL_ENV%
echo ✅ Python Path: %VIRTUAL_ENV%\Scripts\python.exe
echo.

REM Run the launcher with the venv Python
"%VIRTUAL_ENV%\Scripts\python.exe" launcher\main.py

echo.
echo 🎯 Press any key to exit...
pause > nul
