@echo off
echo Testing core import hook functionality...
echo ========================================

cd /d "f:\CODE\TKA"

REM Run the quick test
python test_quick_core_import.py

echo.
echo Test completed. If you see success messages above, the core import hook is working!
echo.
echo You can now use 'from core.glassmorphism_styler import GlassmorphismStyler' 
echo in any file within your TKA project without worrying about relative imports.

pause
