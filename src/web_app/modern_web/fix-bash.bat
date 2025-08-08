@echo off
echo Fixing bash configuration...

REM Add Git to PATH at the beginning
setx PATH "C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin;%PATH%" >nul 2>&1

REM Disable Windows Apps bash
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\bash.exe" (
    move "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\bash.exe" "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\bash.exe.disabled" >nul 2>&1
)

REM Create doskey alias for bash
reg add "HKEY_CURRENT_USER\Software\Microsoft\Command Processor" /v AutoRun /t REG_SZ /d "doskey bash=C:\Program Files\Git\bin\bash.exe $*" /f >nul 2>&1

echo.
echo ✅ Bash configuration fixed!
echo ✅ You can now use 'npm run dev' directly in any new terminal
echo.
echo Please close this terminal and open a new one, then try:
echo   npm run dev
echo.
pause
