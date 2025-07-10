@echo off
echo Activating TKA virtual environment...
call .venv\Scripts\activate.bat
echo.
echo ✅ Virtual environment activated!
echo Python executable: %VIRTUAL_ENV%\Scripts\python.exe
echo.
echo You can now run:
echo   python main.py
echo   pip install [package]
echo   pytest
echo.
echo To deactivate, type: deactivate
