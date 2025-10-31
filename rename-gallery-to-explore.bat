@echo off
echo ================================================
echo Explore to Explore Folder Rename Script
echo ================================================
echo.
echo IMPORTANT: Close VS Code and all IDEs before running this!
echo Press Ctrl+C to cancel, or
pause

cd /d "%~dp0"

echo Renaming main folder...
git mv "src\lib\modules\Explore" "src\lib\modules\explore"
if %errorlevel% neq 0 (
    echo Git mv failed, trying regular move...
    move "src\lib\modules\Explore" "src\lib\modules\explore"
)

echo.
echo ================================================
echo Folder renamed successfully!
echo ================================================
echo.
echo Next steps:
echo 1. Open your IDE
echo 2. Let it re-index the project
echo 3. Run: npm run check
echo.
pause
