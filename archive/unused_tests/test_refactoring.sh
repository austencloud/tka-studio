#!/bin/bash
# Shell script to test the refactoring
# This tries different Python commands until one works

echo "🧪 Testing refactoring with different Python commands..."
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Try different Python commands
if command_exists py; then
    echo "✅ Using 'py' command"
    py test_refactoring.py
elif command_exists python3; then
    echo "✅ Using 'python3' command"
    python3 test_refactoring.py
elif command_exists python; then
    echo "✅ Using 'python' command"
    python test_refactoring.py
elif [ -f "/c/Users/Austen/AppData/Local/Programs/Python/Python313/python.exe" ]; then
    echo "✅ Using full Python path"
    "/c/Users/Austen/AppData/Local/Programs/Python/Python313/python.exe" test_refactoring.py
else
    echo "❌ No Python interpreter found!"
    echo "Please install Python or check your PATH environment variable."
    echo
    echo "You can try:"
    echo "  - Install Python from python.org"
    echo "  - Use Windows Store Python"
    echo "  - Check your PATH environment variable"
    exit 1
fi
