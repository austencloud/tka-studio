#!/usr/bin/env python3
"""
Environment diagnostic script.
"""

import os
import sys

print("=" * 50)
print("🔧 PYTHON ENVIRONMENT DIAGNOSTIC")
print("=" * 50)

print(f"🐍 Python executable: {sys.executable}")
print(f"📦 Python version: {sys.version}")
print(f"📁 Current working directory: {os.getcwd()}")
print("🛤️  Python path (first 5 entries):")
for i, path in enumerate(sys.path[:5]):
    print(f"   {i + 1}. {path}")

print("\n🔍 Environment variables:")
print(f"   PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"   VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

print("\n📦 Checking key imports:")
imports_to_test = [
    ("sys", "sys"),
    ("os", "os"),
    ("pathlib", "pathlib"),
    ("PyQt6.QtWidgets", "PyQt6.QtWidgets"),
    ("PyQt6.QtCore", "PyQt6.QtCore"),
]

for name, module in imports_to_test:
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError as e:
        print(f"   ❌ {name}: {e}")

print("\n🏁 Diagnostic complete!")
print("=" * 50)
