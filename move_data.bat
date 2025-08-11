@echo off
REM TKA Browse Data Migration Script - Batch
REM Run this from the TKA root directory: F:\CODE\TKA

echo 🚀 Starting TKA Browse Data Migration...

REM Define paths
set "SOURCE_DICT=F:\CODE\TKA\data\dictionary"
set "SOURCE_THUMBS=F:\CODE\TKA\browse_thumbnails"
set "DEST_DICT=F:\CODE\TKA\src\web_app\modern_web\static\dictionary"
set "DEST_THUMBS=F:\CODE\TKA\src\web_app\modern_web\static\browse_thumbnails"

echo 📁 Copying sequence dictionary...
if exist "%SOURCE_DICT%" (
    robocopy "%SOURCE_DICT%" "%DEST_DICT%" /E /IS /IT
    echo ✅ Dictionary copied successfully
) else (
    echo ❌ Source dictionary not found: %SOURCE_DICT%
)

echo 🖼️ Copying browse thumbnails...
if exist "%SOURCE_THUMBS%" (
    robocopy "%SOURCE_THUMBS%" "%DEST_THUMBS%" /E /IS /IT
    echo ✅ Thumbnails copied successfully
) else (
    echo ❌ Source thumbnails not found: %SOURCE_THUMBS%
)

echo 📊 Checking results...
if exist "%DEST_DICT%" (
    for /f %%i in ('dir "%DEST_DICT%" /s /b /a-d ^| find /c /v ""') do set DICT_COUNT=%%i
    echo    • Dictionary files: !DICT_COUNT!
)

if exist "%DEST_THUMBS%" (
    for /f %%i in ('dir "%DEST_THUMBS%" /b /a-d ^| find /c /v ""') do set THUMB_COUNT=%%i
    echo    • Thumbnail files: !THUMB_COUNT!
)

echo 🎉 Browse data migration complete!
echo.
echo 💡 Next steps:
echo    1. Run 'npm run dev' to start the web app
echo    2. Check the Browse tab to see your sequences!
echo.
pause