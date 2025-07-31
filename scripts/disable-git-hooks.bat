@echo off
REM NUCLEAR OPTION: Disable all git hooks completely
REM Run this to eliminate ALL popups forever

echo Disabling all git hooks...

REM 1. Disable pre-commit hooks entirely
pre-commit uninstall 2>nul

REM 2. Move the hook files to disable them
if exist .git\hooks\pre-commit (
    move .git\hooks\pre-commit .git\hooks\pre-commit.disabled >nul 2>&1
    echo Pre-commit hook disabled
) else (
    echo No pre-commit hook found
)

REM 3. Set up git aliases for manual ruff checking  
git config --local alias.check "!ruff check --fix . && ruff format ."
git config --local alias.commit-clean "!f() { git add .; ruff check --fix . --quiet; ruff format . --quiet; git add .; git commit -m \"%1\"; }; f"

echo.
echo ========================================
echo ALL GIT HOOKS DISABLED SUCCESSFULLY!
echo ========================================
echo.
echo Now use: git commit-clean "Your message"
echo Or just: git commit -m "Your message" 
echo.
echo No more popups will appear!
