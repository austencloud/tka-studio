#!/bin/bash

# Custom pre-commit script that auto-fixes and auto-stages
# Place this in .git/hooks/pre-commit (make executable)

# Get list of staged Python files
STAGED_PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$STAGED_PYTHON_FILES" ]; then
    echo "Running ruff on staged Python files..."
    
    # Run ruff check with auto-fix
    ruff check --fix $STAGED_PYTHON_FILES
    
    # Run ruff format
    ruff format $STAGED_PYTHON_FILES
    
    # Auto-stage the fixed files
    git add $STAGED_PYTHON_FILES
    
    echo "Ruff fixes applied and staged automatically."
fi

# Always exit successfully (never block commits)
exit 0
