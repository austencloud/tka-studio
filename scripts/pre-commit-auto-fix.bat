@echo off
REM Custom pre-commit script that auto-fixes and auto-stages (Windows)
REM Place this in .git/hooks/pre-commit.bat (or replace the existing pre-commit)

REM Get list of staged Python files
for /f "tokens=*" %%i in ('git diff --cached --name-only --diff-filter=ACM ^| findstr "\.py$"') do (
    set STAGED_PYTHON_FILES=%%i
    goto :process_files
)
goto :end

:process_files
echo Running ruff on staged Python files...

REM Run ruff check with auto-fix
ruff check --fix .

REM Run ruff format
ruff format .

REM Auto-stage all Python files that were modified
git add -u *.py

echo Ruff fixes applied and staged automatically.

:end
REM Always exit successfully (never block commits)
exit /b 0
